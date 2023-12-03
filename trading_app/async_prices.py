import requests
import json
import asyncio, asyncpg, asyncio, aiohttp
import time
from datetime import datetime
from trading_app.config import settings
import traceback
from decimal import Decimal
import pytz

url = "https://api.polygon.io/v2/aggs/ticker/{}/range/1/day/2023-11-01/2023-11-02?apiKey={}"


async def write_to_db(connection, params):
    try:
        await connection.copy_records_to_table('stock_price', records=params)
    except Exception as e:
        print(f"Error writing to DB: {e}")
        print(f"Data causing error: {params}")
        raise


async def get_price(pool, stock_id, url):
    try:
        async with pool.acquire() as connection:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url) as response:
                    resp = await response.read()
                    response = json.loads(resp)
                    params = [(stock_id, datetime.fromtimestamp(bar['t'] / 1000.0),
                               round(bar['o'], 2), round(bar['h'], 2), round(bar['l'], 2),
                               round(bar['c'], 2), round(bar['v'], 2)) for bar in response['results']]

                    await write_to_db(connection, params)

    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))
        traceback.print_exc()


async def get_prices(pool, symbol_urls):
    try:
        # schedule aiohttp requests to run concurrently for all symbols
        ret = await asyncio.gather(*[get_price(pool, stock_id, symbol_urls[stock_id]) for stock_id in symbol_urls])
        print("Finalized all. Returned  list of {} outputs.".format(len(ret)))
    except Exception as e:
        print(e)
        traceback.print_exc()


async def get_stocks():
    # create database connection pool
    pool = await asyncpg.create_pool(user=settings.database_username,
                                     password=settings.database_password,
                                     database=settings.database_name,
                                     host=settings.database_hostname,
                                     command_timeout=60)

    # get a connection
    async with (pool.acquire() as connection):
        stocks = await connection.fetch("SELECT * FROM stock")

        symbol_urls = {}
        for stock in stocks:
            symbol_urls[stock['id']] = url.format(stock['symbol'], settings.polygon_key)

    await get_prices(pool, symbol_urls)


start = time.time()
asyncio.run(get_stocks())
end = time.time()

print("Took {} seconds.".format(end - start))
