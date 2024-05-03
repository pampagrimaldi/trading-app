import asyncio
import aiohttp
from datetime import datetime
import pytz
from sqlalchemy import select
from trading_app.database import SessionLocalAsync, SessionLocal
from trading_app.models import Stock, StockPrice
from aiohttp.client_exceptions import ClientResponseError
import time
import random
from tqdm.asyncio import trange
from tqdm import tqdm
import logging
import os
import tulipy as ti
import numpy as np


# todo: fix the additional error logging

# Set up logging
log_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'logs', 'populate_stock_prices.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Constants
BASE_URL = "https://localhost:5002/v1/api/iserver/marketdata/history"
# PERIOD = "3y"
PERIOD = "1w"
BAR = "1d"
SEM_LIMIT = 40  # Semaphore limit
CHUNK_SIZE = 40  # Number of stocks to process in parallel

# Semaphore for rate-limiting
semaphore = asyncio.Semaphore(SEM_LIMIT)


# Fetch historical data for a stock
async def fetch_historical_data(session, conid, max_retries=5):
    """
        Fetch historical data for a stock.

        Args:
            session (aiohttp.ClientSession): The session to use for making HTTP requests.
            conid (int): The contract ID of the stock.
            max_retries (int, optional): The maximum number of retries if a request fails. Defaults to 1.

        Returns:
            dict: The JSON response from the server, or None if an error occurred.
    """
    url = f"{BASE_URL}?conid={conid}&period={PERIOD}&bar={BAR}"
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
                elif e.status ==503:
                    print(f"Service unavailable, retrying in 1 second...")
                    await asyncio.sleep(1 ** retries + random.uniform(0, 1))
                    retries +=1
                    continue
                elif e.status == 500:
                    # Silently handle 500 errors
                    return None
                else:
                    print(f"Error fetching price data for conid {conid}: {e.status}")
                    return None
    print(f"Max retries hit for conid {conid}")
    return None


# Process historical data for each stock
async def process_stock_data(session, stock_id, conid):
    """
        Process historical data for a stock.

        Args:
            session (aiohttp.ClientSession): The session to use for making HTTP requests.
            stock_id (int): The ID of the stock.
            conid (int): The contract ID of the stock.

        Returns:
            list: A list of StockPrice instances, or an empty list if an error occurred.
    """
    try:
        historical_data = await fetch_historical_data(session, conid, max_retries=5)

        if historical_data is None:
            return []

        stock_prices = []
        closing_prices = []
        async with SessionLocalAsync() as db_session:  # Create a new SQLAlchemy session
            for data_point in historical_data["data"]:
                dt = datetime.fromtimestamp(data_point["t"] / 1000)
                # Check if a record with the same stock_id and dt already exists
                existing_price = await db_session.execute(
                    select(StockPrice).where((StockPrice.stock_id == stock_id) & (StockPrice.dt == dt)))
                existing_price = existing_price.scalar_one_or_none()
                if existing_price:
                    # Update the existing record
                    existing_price.open = data_point["o"]
                    existing_price.close = data_point["c"]
                    existing_price.high = data_point["h"]
                    existing_price.low = data_point["l"]
                    existing_price.volume = data_point["v"]
                else:
                    # Create a new record
                    stock_prices.append(StockPrice(stock_id=stock_id,
                                                   dt=dt,
                                                   open=data_point["o"],
                                                   close=data_point["c"],
                                                   high=data_point["h"],
                                                   low=data_point["l"],
                                                   volume=data_point["v"]))
                closing_prices.append(data_point["c"])
        return stock_prices, closing_prices
    except Exception as e:
        print(f"Error fetching historical data for {conid}: {e}")
        logging.error(f"Error fetching historical data for {conid}: {e}", exc_info=False)
        return []


# Bulk insert stock price data into the database
async def bulk_insert_prices(stock_prices):
    """
        Bulk insert stock price data into the database.

        Args:
            stock_prices (list): A list of StockPrice instances to insert.
    """
    async with SessionLocalAsync() as session:
        async with session.begin():
            session.add_all(stock_prices)


async def main():
    """
        The main function of the script. It orchestrates the entire process of fetching historical data for each stock,
        processing the data, and then saving the data to the database. It does this by calling the other functions in the
        script in the correct order.
    """
    async with aiohttp.ClientSession() as session:
        async with SessionLocalAsync() as db_session:
            # debug: test on a single stock
            # result = await db_session.execute(select(Stock).filter(Stock.symbol == 'BHP'))
            result = await db_session.execute(select(Stock))
            stocks = result.scalars().all()

        total_chunks = (len(stocks) + CHUNK_SIZE - 1) // CHUNK_SIZE

        # Initialize a counter for the total number of records included
        total_records_included = 0

        # Process stocks in chunks with progress bar
        async for i in trange(0, len(stocks), CHUNK_SIZE, desc="Processing Stocks", total=total_chunks):
            chunk = stocks[i:i + CHUNK_SIZE]
            tasks = [process_stock_data(session, stock.id, stock.conid) for stock in chunk]
            all_results_chunk = await asyncio.gather(*tasks)
            all_prices_chunk = [result[0] for result in all_results_chunk if result]
            all_closing_prices_chunk = [result[1] for result in all_results_chunk if result]

            # Increment the counter by the number of records included in this chunk
            total_records_included += len(all_prices_chunk)

            # Bulk insert for each chunk
            for prices in all_prices_chunk:
                await bulk_insert_prices(prices)

            # Sleep for 1 second between requests to avoid throttling
            await asyncio.sleep(1)

        # Calculate the SMAs and RSI for each stock
        for stock in tqdm(stocks, desc="Calculating Technical Indicators"):
            # Create a new session
            with SessionLocal() as db:
                try:
                    stock_prices = (db
                                    .query(StockPrice)
                                    .filter(StockPrice.stock_id == stock.id)
                                    .order_by(StockPrice.dt.desc())
                                    .limit(50)  # Get the 50 most recent prices
                                    .all())

                    closing_prices = [price.close for price in stock_prices]
                    # closing prices array
                    cp_array = np.array(closing_prices, dtype='d')
                    # Calculate the SMAs and RSI
                    sma_20 = ti.sma(cp_array, period=20)[-1] if len(cp_array) >= 20 else None
                    sma_50 = ti.sma(cp_array, period=50)[-1] if len(cp_array) >= 50 else None
                    rsi_14 = ti.rsi(cp_array, period=14)[-1] if len(cp_array) >= 14 else None

                    # Update the latest StockPrice instance with the calculated SMA and RSI values
                    stock_prices[0].sma20 = sma_20
                    stock_prices[0].sma50 = sma_50
                    stock_prices[0].rsi14 = rsi_14

                    # Commit the changes to the database
                    db.commit()
                except Exception as e:
                    logging.error(f"Error calculating SMA/RSI for {stock.symbol}: {e}", exc_info=False)

        # Log the total number of records included
        logging.info('Total number of records included: %s', total_records_included)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    logging.info('Total time taken %s seconds', round(end_time - start_time, 2))
