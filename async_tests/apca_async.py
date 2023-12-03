from enum import Enum
import time
import alpaca_trade_api as tradeapi
import asyncio
import os
import pandas as pd
from alpaca_trade_api.rest import TimeFrame, URL
from alpaca_trade_api.rest_async import AsyncRest
from trading_app.config import settings

NY = 'America/New_York'

class DataType(str, Enum):
    Bars = "Bars"
    Trades = "Trades"
    Quotes = "Quotes"


# Define the new function for processing and logging responses
async def process_and_log_responses(results, symbols):
    bad_requests = 0
    example_printed = False  # Flag to ensure only one example is printed
    for response in results:
        ticker_symbol = response[0]
        df = response[1]
        if isinstance(response, Exception):
            print(f"Got an error: {response}")
        else:
            try:
                if not response or (isinstance(df, pd.DataFrame) and df.empty):
                    bad_requests += 1
                    print(f"Empty response for symbol: {ticker_symbol}")
                else:
                    if not example_printed:

                        print(f"Example response for symbol {ticker_symbol}:", df.head(5))
                        print(f"Dataframe structure:", type(df.info()))
                        example_printed = True
            except Exception as e:
                print(f"Error processing response for symbol {ticker_symbol}: {e}")

    print(f"Total of {len(results)} responses, and {bad_requests} empty responses.")


async def get_historic_bars(symbols, data_type: DataType, start, end,
                                 timeframe: TimeFrame = None):

    msg = f"Getting {data_type} data for {len(symbols)} symbols"
    msg += f", timeframe: {timeframe}" if timeframe else ""
    msg += f" between dates: start={start}, end={end}"
    print(msg)

    step_size = 200
    results = []
    for i in range(0, len(symbols), step_size):
        tasks = []
        for symbol in symbols[i:i+step_size]:
            tasks.append(rest.get_bars_async(symbol, start, end, timeframe.value, adjustment='raw'))

        results.extend(await asyncio.gather(*tasks, return_exceptions=True))

    # Call the new function to process and log responses
    await process_and_log_responses(results, symbols)


async def main(symbols):
    start = pd.Timestamp('2022-01-01', tz=NY).date().isoformat()
    end = pd.Timestamp('2023-11-30', tz=NY).date().isoformat()
    timeframe: TimeFrame = TimeFrame.Minute
    await get_historic_bars(symbols, DataType.Bars, start, end, timeframe)


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
    #todo: change stock list for sql query
    symbols = [el.symbol for el in assets if el.status == "active" and el.tradable]
    symbols = symbols[:10]
    asyncio.run(main(symbols))
    print(f"took {time.time() - start_time} sec")