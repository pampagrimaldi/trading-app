import asyncio
import aiohttp
from datetime import datetime
from sqlalchemy import select
from trading_app.database import SessionLocalAsync
from trading_app.models import Stock, StockPrice
from aiohttp.client_exceptions import ClientResponseError
import time
import random


# Constants
BASE_URL = "https://localhost:5002/v1/api/iserver/marketdata/history"
PERIOD = "1y"
BAR = "1d"
SEM_LIMIT = 5  # Semaphore limit

# Semaphore for rate-limiting
semaphore = asyncio.Semaphore(SEM_LIMIT)


# Fetch historical data for a stock
async def fetch_historical_data(session, conid, max_retries=1):
    url = f"{BASE_URL}?conid={conid}&period={PERIOD}&bar={BAR}"
    print("=== debugging url ===")
    print(url)
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
                else:
                    print(f"Error fetching price data for conid {conid}: {e.status}")
                    return None
    print(f"Max retries hit for conid {conid}")
    return None


# Process historical data for each stock
async def process_stock_data(session, stock_id, conid):
    try:
        historical_data = await fetch_historical_data(session, conid, max_retries=2)
        return [
            StockPrice(
                stock_id=stock_id,
                dt=datetime.fromtimestamp(data_point["t"] / 1000),
                open=data_point["o"],
                close=data_point["c"],
                high=data_point["h"],
                low=data_point["l"],
                volume=data_point["v"],
                trade_count=0  # If trade count is not available
            )
            for data_point in historical_data["data"]
        ]
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
        # Fetch existing stock symbols from the database
        async with SessionLocalAsync() as db_session:
            result = await db_session.execute(select(Stock))
            stocks = result.scalars().all()
            # debug by only testing on 1 stock
            stocks = [stocks[0]]
            for each in stocks:
                print(f'stock conid {each.conid} and ib_symbol {type(each.ib_symbol)}')

        # Process each stock symbol
        tasks = [process_stock_data(session, stock.id, stock.conid) for stock in stocks]
        all_prices = await asyncio.gather(*tasks)
        # Flatten list of lists
        all_prices = [price for sublist in all_prices for price in sublist if sublist]

        # Bulk insert into the database
        await bulk_insert_prices(all_prices)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f'Total time taken {end_time - start_time} seconds')
