import asyncio
from sqlalchemy import select
from aiohttp.client_exceptions import ClientResponseError
import aiohttp
from bs4 import BeautifulSoup
import time
from trading_app.database import SessionLocalAsync
from trading_app import models
from tqdm.asyncio import tqdm
import logging
import random

# Set logging level
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

# Async Scraper

base_url = "https://www.interactivebrokers.com/"
first_page_url = "/en/index.php?f=2222&exch=asx&showcategories=STK&p=&ptab=&cc=&limit=100&page=1"

# Dictionary to store the results
stocks_dict = {}
processed_symbols = set()


async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()


async def parse_page(html):
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
    # Check if the symbol has already been processed
    if symbol in processed_symbols:
        print(f"Duplicate symbol found: {symbol}")
        return
    processed_symbols.add(symbol)

    # Database check for existing stock with the same ib_symbol
    async with SessionLocalAsync() as check_session:
        result = await check_session.execute(select(models.Stock).where(models.Stock.ib_symbol == ib_symbol))
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
    async with SessionLocalAsync() as session:
        async with session.begin():
            try:
                # Check if the stock with this ib_symbol already exists
                result = await session.execute(select(models.Stock).where(models.Stock.ib_symbol == ib_symbol))
                existing_stock = result.scalar_one_or_none()

                if not existing_stock:
                    new_stock = models.Stock(
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
    async with SessionLocalAsync() as session:
        result = await session.execute(select(models.Stock.ib_symbol))
        return {row[0] for row in result.fetchall()}


async def main():
    async with aiohttp.ClientSession() as session:
        # Scrape symbols
        print('Scraping symbols...')
        symbols_data = await scrape_symbols()
        print('Scraping complete.')

        # Fetch existing ib_symbols from the database
        existing_ib_symbols = await fetch_existing_ib_symbols()

        # Process each symbol in batches
        batch_size = 40
        total_batches = (len(symbols_data) + batch_size - 1) // batch_size

        print('Processing symbols...')
        async for i in tqdm(range(0, len(symbols_data), batch_size), total=total_batches, desc="Processing symbols"):
            # batch excludes symbols that already exist in the database
            batch = [(ib_symbol, symbol) for ib_symbol, symbol in symbols_data[i:i + batch_size]
                     if ib_symbol not in existing_ib_symbols]
            # gather all the tasks in the batch
            tasks = [process_stock_data(session, ib_symbol, symbol) for ib_symbol, symbol in batch]
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)  # Wait 1 second between each batch

        print('Processing complete.')


if __name__ == '__main__':

    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f'Total time taken {end_time - start_time} seconds')
