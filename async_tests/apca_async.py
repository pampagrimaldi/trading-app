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


def get_data_method(data_type: DataType):
    if data_type == DataType.Bars:
        return rest.get_bars_async
    elif data_type == DataType.Trades:
        return rest.get_trades_async
    elif data_type == DataType.Quotes:
        return rest.get_quotes_async
    else:
        raise Exception(f"Unsupoported data type: {data_type}")


async def get_historic_data_base(symbols, data_type: DataType, start, end,
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
            args = [symbol, start, end, timeframe.value]
            tasks.append(get_data_method(data_type)(*args))

        results.extend(await asyncio.gather(*tasks, return_exceptions=True))

    bad_requests = 0
    for index, response in enumerate(results):
        if isinstance(response, Exception):
            print(f"Got an error: {response}")
        else:
            try:
                # Check if response is as expected and process it
                if not response:  # Adjust this condition based on actual response structure
                    bad_requests += 1
                    print(f"Empty response for symbol: {symbols[index % len(symbols)]}")
                # else handle valid response
            except Exception as e:
                print(f"Error processing response for symbol {symbols[index % len(symbols)]}: {e}")

    print(f"Total of {len(results)} {data_type}, and {bad_requests} "
          f"empty responses.")


async def get_historic_bars(symbols, start, end, timeframe: TimeFrame):
    await get_historic_data_base(symbols, DataType.Bars, start, end, timeframe)


async def main(symbols):
    start = pd.Timestamp('2022-01-01', tz=NY).date().isoformat()
    end = pd.Timestamp('2023-11-30', tz=NY).date().isoformat()
    timeframe: TimeFrame = TimeFrame.Minute
    await get_historic_bars(symbols, start, end, timeframe)


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
    symbols = [el.symbol for el in api.list_assets(status='active')]
    # symbols = symbols[:200]
    asyncio.run(main(symbols))
    print(f"took {time.time() - start_time} sec")