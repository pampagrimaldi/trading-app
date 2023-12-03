import asyncio
import aiohttp
import time
from trading_app.config import settings

url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol={}&apikey={}'

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

results = []

start = time.time()





# create loop to fetch each symbols synchronously
async def get_symbols():
    async with aiohttp.ClientSession() as session:
        for symbol in symbols:
            print(f'Working on symbol {symbol}')
            # this will return a coroutine object, which needs to be waited
            # the issue is that this is still semi-synchronous, as we're sending a request one at a time.
            # it would be faster to rapid send all at once.
            response = await session.get(url.format(symbol, settings.alphavantage_key))
            results.append(await response.json())
        print('Yoy did it!')


# get_symbols()
loop = asyncio.run(get_symbols())

end = time.time()
# get time
print(f'Total time taken {end - start}')
