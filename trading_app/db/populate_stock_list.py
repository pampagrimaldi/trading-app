"""
This script is used to populate a database with stock data.

It scrapes stock symbols from the Interactive Brokers website, fetches contract details for each symbol from
a local server,and then saves the data to a database.

To run this script, use the following command: python -m trading_app.db.populate_db
"""
import asyncio
from sqlalchemy import select
from aiohttp.client_exceptions import ClientResponseError
import aiohttp
from bs4 import BeautifulSoup
import time
from trading_app.database import SessionLocalAsync
from trading_app.models import Stock
from tqdm.asyncio import tqdm
import logging
import os
import random

# Set logging level
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

# Set up logging
log_file_path = os.path.join(os.path.dirname(__file__), '..', '..',  'logs', 'populate_stock_list.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Async Scraper

base_url = "https://www.interactivebrokers.com/"
first_page_url = "/en/index.php?f=2222&exch=asx&showcategories=STK&p=&ptab=&cc=&limit=100&page=1"

# Dictionary to store the results
stocks_dict = {}
processed_symbols = set()


async def fetch_page(session, url):
    """
        Fetches the HTML content of a given URL using an aiohttp session.

        Parameters:
        session (aiohttp.ClientSession): The aiohttp session to use for the request.
        url (str): The URL to fetch.

        Returns:
        str: The HTML content of the URL.
    """
    async with session.get(url) as response:
        return await response.text()


async def parse_page(html):
    """
        Parses the HTML content of a page using BeautifulSoup. It extracts the Interactive Brokers symbol and the
        corresponding stock symbol from the page and stores them in a dictionary.

        Parameters:
        html (str): The HTML content to parse.

        Returns:
        BeautifulSoup: A BeautifulSoup object representing the parsed HTML.
    """
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('div', class_='table-responsive no-margin').find('table')
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if columns:
            ib_symbol = columns[0].text.strip()
            symbol = columns[2].text.strip()

            # Update the dictionary
            stocks_dict[ib_symbol] = symbol
    return soup


async def get_page_urls(session, first_page_url):
    """
        Generates the URLs of all the pages that need to be scraped. It does this by fetching the first page, parsing it
        to find the total number of pages, and then generating the URL for each page.

        Parameters:
        session (aiohttp.ClientSession): The aiohttp session to use for the request.
        first_page_url (str): The URL of the first page.

        Returns:
        list: A list of URLs.
    """
    urls = [first_page_url]
    first_page_html = await fetch_page(session, first_page_url)
    soup = await parse_page(first_page_html)

    # Logic to determine the total number of pages
    pagination = soup.find('ul', class_='pagination')
    if pagination:
        # Assuming that the last page number is in the last 'li' before the 'Next' button
        last_page_number = int(pagination.find_all('li')[-2].text)
        for i in range(2, last_page_number + 1):
            page_url = base_url + f"/en/index.php?f=2222&exch=asx&showcategories=STK&p=&ptab=&cc=&limit=100&page={i}"
            urls.append(page_url)

    return urls


async def scrape_symbols():
    """
        Scrapes the symbols of stocks from the Interactive Brokers website. It does this by fetching
        and parsing each page, and then extracting the symbols from each page.

        Returns:
        list: A list of tuples, where each tuple contains an Interactive Brokers symbol
        and the corresponding stock symbol.
    """
    async with aiohttp.ClientSession() as session:
        page_urls = await get_page_urls(session, base_url + first_page_url)
        tasks = [asyncio.create_task(fetch_page(session, url)) for url in page_urls]
        pages = await asyncio.gather(*tasks)

        for page_html in pages:
            await parse_page(page_html)

    return [(ib_symbol, symbol) for ib_symbol, symbol in stocks_dict.items()]

# Semaphore to limit the number of requests
semaphore = asyncio.Semaphore(40)


async def fetch_contract_details(session, symbol, max_retries=5):
    """
        Fetches the contract details for a given stock symbol from a local server. It does this by sending a GET request
        to the server and then parsing the JSON response.

        Parameters:
        session (aiohttp.ClientSession): The aiohttp session to use for the request.
        symbol (str): The stock symbol to fetch contract details for.
        max_retries (int, optional): The maximum number of retries if the request fails. Defaults to 5.

        Returns:
        dict: A dictionary containing the contract details.
    """
    url = f"https://localhost:5002/v1/api/trsrv/stocks?symbols={symbol}"
    retries = 0
    while retries < max_retries:
        async with semaphore, session.get(url, ssl=False) as response:
            try:
                response.raise_for_status()
                if 'application/json' not in response.headers.get('Content-Type', ''):
                    print(f"Non-JSON response received: {await response.text()}")
                    return None
                return await response.json()
            except ClientResponseError as e:
                if e.status == 429:
                    retries += 1
                    retry_after = int(response.headers.get('Retry-After', '1'))
                    print(f"Rate limit hit, retrying in {retry_after} seconds...")
                    await asyncio.sleep(retry_after)
                else:
                    print(f"Error fetching details for {symbol}: {e.status}")
                    return None
    print(f"Max retries hit for symbol {symbol}")
    return None


async def process_stock_data(session, ib_symbol, symbol, batch_delay=1, max_retries=5):
    """
        Processes the data for a given stock. It does this by fetching the contract details for the stock, checking if the
        stock already exists in the database, and then saving the stock to the database if it doesn't already exist.

        Parameters:
        session (aiohttp.ClientSession): The aiohttp session to use for the request.
        ib_symbol (str): The Interactive Brokers symbol of the stock.
        symbol (str): The stock symbol.
        batch_delay (int, optional): The delay between each batch of requests in seconds. Defaults to 1.
        max_retries (int, optional): The maximum number of retries if the request fails. Defaults to 5.
    """

    # Check if the symbol has already been processed
    if symbol in processed_symbols:
        print(f"Duplicate symbol found: {symbol}")
        return
    processed_symbols.add(symbol)

    # Database check for existing stock with the same ib_symbol
    async with SessionLocalAsync() as check_session:
        result = await check_session.execute(select(Stock).where(Stock.ib_symbol == ib_symbol))
        if result.scalar_one_or_none():
            print(f"Stock with ib_symbol {ib_symbol} already exists. Skipping.")
            return

    retries = 0
    while retries < max_retries:
        try:
            stock_data = await fetch_contract_details(session, symbol)
            if stock_data:
                for stock_info in stock_data.get(symbol, []):
                    if stock_info.get("assetClass") == "STK":
                        for contract in stock_info.get("contracts", []):
                            if contract.get("exchange") == "ASX":
                                await save_to_database(ib_symbol, symbol, stock_info, contract)
                break
            else:
                raise Exception("No data received")
        except Exception as e:
            print(f"Error fetching details for {symbol}: {e}")
            retries += 1
            await asyncio.sleep(batch_delay * (2 ** retries) + random.uniform(0, 1))


async def save_to_database(ib_symbol, symbol, stock_info, contract):
    """
        Saves a stock to the database. It does this by creating a new Stock object with the given data and then adding the
        object to the database session.

        Parameters:
        ib_symbol (str): The Interactive Brokers symbol of the stock.
        symbol (str): The stock symbol.
        stock_info (dict): A dictionary containing the stock information.
        contract (dict): A dictionary containing the contract details.
    """

    async with SessionLocalAsync() as session:
        async with session.begin():
            try:
                # Check if the stock with this ib_symbol already exists
                result = await session.execute(select(Stock).where(Stock.ib_symbol == ib_symbol))
                existing_stock = result.scalar_one_or_none()

                if not existing_stock:
                    new_stock = Stock(
                        ib_symbol=ib_symbol,
                        symbol=symbol,
                        name=stock_info.get("name"),
                        asset_class=stock_info.get("assetClass"),
                        conid=contract.get("conid"),
                        exchange=contract.get("exchange"),
                        is_us=contract.get("isUS")
                    )
                    session.add(new_stock)
            except Exception as e:
                await session.rollback()  # Rollback the transaction in case of an error
                print(f"Error while saving to database: {e}")
                raise  # Optionally re-raise the exception to handle it at a higher level


async def fetch_existing_ib_symbols():
    """
        Fetches the Interactive Brokers symbols of all the stocks that already exist in the database. It does this by
        executing a SELECT query on the Stock table and then extracting the Interactive Brokers symbols from the results.

        Returns:
        set: A set of Interactive Brokers symbols.
    """
    async with SessionLocalAsync() as session:
        result = await session.execute(select(Stock.ib_symbol))
        return {row[0] for row in result.fetchall()}


async def main():
    """
        The main function of the script. It orchestrates the entire process of scraping the symbols from the Interactive
        Brokers website, processing the data for each symbol, and then saving the data to the database. It does this by
        calling the other functions in the script in the correct order.
    """
    async with aiohttp.ClientSession() as session:
        # Scrape symbols
        logging.info('Scraping symbols...')
        symbols_data = await scrape_symbols()
        logging.info('Scraping complete.')

        # Fetch existing ib_symbols from the database
        existing_ib_symbols = await fetch_existing_ib_symbols()

        # Process each symbol in batches
        batch_size = 40
        total_batches = (len(symbols_data) + batch_size - 1) // batch_size

        logging.info('Processing symbols...')
        async for i in tqdm(range(0, len(symbols_data), batch_size), total=total_batches, desc="Processing symbols"):
            # batch excludes symbols that already exist in the database
            batch = [(ib_symbol, symbol) for ib_symbol, symbol in symbols_data[i:i + batch_size]
                     if ib_symbol not in existing_ib_symbols]
            # gather all the tasks in the batch
            tasks = [process_stock_data(session, ib_symbol, symbol) for ib_symbol, symbol in batch]
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)  # Wait 1 second between each batch

        logging.info('Processing complete. Updated %s stocks.', len(processed_symbols))


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    logging.info('Total time taken %s seconds', round(end_time - start_time, 2))
