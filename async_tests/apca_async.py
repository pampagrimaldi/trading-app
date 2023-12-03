from enum import Enum
import time
import alpaca_trade_api as tradeapi
import asyncio
import pandas as pd
from alpaca_trade_api.rest import TimeFrame
from alpaca_trade_api.rest_async import AsyncRest
from trading_app.config import settings
from io import BytesIO, StringIO
import asyncpg
import logging


class DataType(str, Enum):
    Bars = "Bars"
    Trades = "Trades"
    Quotes = "Quotes"


# async def write_to_db(connection, table_name, df):
#     # Convert DataFrame to CSV in-memory using StringIO
#     sio = StringIO()
#     df.to_csv(sio, index=False, header=False)
#     sio.seek(0)  # Rewind the buffer
#
#     # Use copy_to_table with StringIO
#     await connection.copy_to_table(table_name, source=sio, format='csv')

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)


async def write_to_db(connection, table_name, df):
    # Log DataFrame structure and first few rows
    logging.debug(f"DataFrame structure: {df.dtypes}")
    logging.debug(f"DataFrame preview: {df.head()}")

    # Convert DataFrame to CSV in-memory using BytesIO
    buffer = BytesIO()
    df.to_csv(buffer, index=False, header=False, mode='wb')
    buffer.seek(0)  # Rewind the buffer

    # Use copy_to_table with BytesIO
    await connection.copy_to_table(table_name, source=buffer, format='csv')


# Define the new function for processing and logging responses
async def process_and_log_responses(pool, results, symbol_to_stock_id):
    bad_requests = 0
    for ticker_symbol, df in results:
        if isinstance(df, Exception):
            print(f"Got an error: {df}")
        elif df.empty:
            bad_requests += 1
            print(f"Empty response for symbol: {ticker_symbol}")
        else:
            try:
                # Adjust the DataFrame and write it to the database
                adjusted_df = adjust_dataframe(ticker_symbol, df, symbol_to_stock_id)
                async with pool.acquire() as connection:
                    await write_to_db(connection, 'stock_price', adjusted_df)
            except Exception as e:
                print(f"Error processing response for symbol {ticker_symbol}: {e}")

    print(f"Total of {len(results)} responses, and {bad_requests} empty responses.")



def adjust_dataframe(ticker_symbol, df, symbol_to_stock_id):
    df['symbol'] = ticker_symbol
    df['stock_id'] = df['symbol'].map(symbol_to_stock_id)
    df['timestamp'] = pd.to_datetime(df.index).tz_convert(None)
    df = df[['stock_id', 'timestamp', 'close', 'high', 'low', 'trade_count', 'open', 'volume', 'vwap']]

    return df


async def get_symbol_to_id_mapping(pool):
    symbol_to_id = {}
    async with pool.acquire() as connection:
        rows = await connection.fetch("SELECT symbol, id FROM public.stock")
        symbol_to_id = {row['symbol']: row['id'] for row in rows}
    return symbol_to_id

async def get_historic_bars(pool, symbols, data_type: DataType, start, end,
                                 timeframe: TimeFrame = None, symbol_to_stock_id=None):
    print(f"Getting {data_type} data for {len(symbols)} symbols between dates: start={start}, end={end}")
    step_size = 200
    results = []
    for i in range(0, len(symbols), step_size):
        tasks = []
        for symbol in symbols[i:i+step_size]:
            task = rest.get_bars_async(symbol, start, end, timeframe.value, adjustment='raw')
            tasks.append(task)

        results.extend(await asyncio.gather(*tasks, return_exceptions=True))

    # Call the new function to process and log responses
    await process_and_log_responses(pool, results, symbol_to_stock_id)


async def main():
    pool = await asyncpg.create_pool(user=settings.database_username,
                                     password=settings.database_password,
                                     database=settings.database_name,
                                     host=settings.database_hostname,
                                     command_timeout=60)
    symbol_to_id = await get_symbol_to_id_mapping(pool)
    start = pd.Timestamp('2022-01-01').date().isoformat()
    end = pd.Timestamp('2023-11-30').date().isoformat()
    timeframe: TimeFrame = TimeFrame.Minute
    symbols = [el.symbol for el in api.list_assets() if el.status == "active" and el.tradable][:10]
    await get_historic_bars(pool, symbols, DataType.Bars, start, end, timeframe, symbol_to_id)


if __name__ == '__main__':

    base_url = "https://paper-api.alpaca.markets"
    feed = "iex"  # change to "sip" if you have a paid account

    rest = AsyncRest(key_id=settings.apca_key,
                     secret_key=settings.apca_secret_key,
                     api_version="v2")

    api = tradeapi.REST(key_id=settings.apca_key,
                        secret_key=settings.apca_secret_key,
                        api_version="v2")
    # start time
    start_time = time.time()
    assets = api.list_assets()
    asyncio.run(main())
    print(f"took {time.time() - start_time} sec")