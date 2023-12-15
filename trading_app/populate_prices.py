import asyncio
import aiohttp
from datetime import datetime
import pytz
from sqlalchemy import select
from trading_app.database import SessionLocalAsync
from trading_app.models import Stock, StockPrice
from aiohttp.client_exceptions import ClientResponseError
import time
import random
from tqdm.asyncio import trange


# todo: review semaphore in combination with upsert - it's not working.

# Constants
BASE_URL = "https://localhost:5002/v1/api/iserver/marketdata/history"
# PERIOD = "3y"
PERIOD = "1m"
BAR = "1d"
SEM_LIMIT = 45  # Semaphore limit
CHUNK_SIZE = 45  # Number of stocks to process in parallel

# Semaphore for rate-limiting
semaphore = asyncio.Semaphore(SEM_LIMIT)


# Fetch historical data for a stock
async def fetch_historical_data(session, conid, max_retries=1):
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
# Process historical data for each stock
async def process_stock_data(session, stock_id, conid):
    try:
        historical_data = await fetch_historical_data(session, conid, max_retries=2)

        if historical_data is None:
            return []

        stock_prices = []
        async with SessionLocalAsync() as db_session:  # Create a new SQLAlchemy session
            for data_point in historical_data["data"]:
                dt = datetime.fromtimestamp(data_point["t"] / 1000)
                # Check if a record with the same stock_id and dt already exists
                existing_price = await db_session.execute(select(StockPrice).where((StockPrice.stock_id == stock_id) & (StockPrice.dt == dt)))
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
        return stock_prices
    except Exception as e:
        print(f"Error fetching historical data for {conid}: {e}")
        return []


# Bulk insert stock price data into the database
async def bulk_insert_prices(stock_prices):
    async with SessionLocalAsync() as session:
        async with session.begin():
            session.add_all(stock_prices)


async def main():
    async with aiohttp.ClientSession() as session:
        async with SessionLocalAsync() as db_session:
            result = await db_session.execute(select(Stock))
            stocks = result.scalars().all()

        total_chunks = (len(stocks) + CHUNK_SIZE - 1) // CHUNK_SIZE

        # Process stocks in chunks with progress bar
        async for i in trange(0, len(stocks), CHUNK_SIZE, desc="Processing Stocks", total=total_chunks):
            chunk = stocks[i:i + CHUNK_SIZE]
            tasks = [process_stock_data(session, stock.id, stock.conid) for stock in chunk]
            all_prices_chunk = await asyncio.gather(*tasks)
            all_prices_chunk = [price for sublist in all_prices_chunk for price in sublist if sublist]

            # Bulk insert for each chunk
            await bulk_insert_prices(all_prices_chunk)

            # Sleep for 1 second between requests to avoid throttling
            await asyncio.sleep(1)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f'Total time taken {end_time - start_time} seconds')