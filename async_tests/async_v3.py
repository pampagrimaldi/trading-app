import asyncio
import aiohttp
import time
from trading_app.config import settings

# random symbols to call
symbols = ['AAPL', 'GOOG', 'TSLA', 'MSFT',
           'AAPL', 'GOOG', 'TSLA', 'MSFT',
           'AAPL', 'GOOG', 'TSLA', 'MSFT',
           'AAPL', 'GOOG', 'TSLA', 'MSFT',
           'AAPL', 'GOOG', 'TSLA', 'MSFT',
           'AAPL', 'GOOG', 'TSLA', 'MSFT',
           'AAPL', 'GOOG', 'TSLA', 'MSFT',
           'AAPL', 'GOOG', 'TSLA', 'MSFT',
           'AAPL', 'GOOG', 'TSLA', 'MSFT',
           'AAPL', 'GOOG', 'TSLA', 'MSFT',
           'AAPL', 'GOOG', 'TSLA', 'MSFT',
           'AAPL', 'GOOG', 'TSLA', 'MSFT']

# formatted api url
url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol={}&apikey={}'

# save results and start time
results = []
start = time.time()


# create loop to fetch each symbols synchronously
async def get_symbols():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(session.get(url.format(symbol, settings.alphavantage_key), ssl=False)) for symbol
                 in symbols]
        responses = await asyncio.gather(*tasks)


# get_symbols()
asyncio.run(get_symbols())

end = time.time()
# get time
print(f'Total time taken {end - start}')
