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


def get_tasks(session):
    """
    list of all objects the api will call.
    :param session:
    :return:
    """
    tasks = []
    for symbol in symbols:
        tasks.append(session.get(url.format(symbol, settings.alphavantage_key)))
    return tasks


# create loop to fetch each symbols synchronously
async def get_symbols():
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            results.append(await response.json())

# get_symbols()
asyncio.run(get_symbols())

end = time.time()
# get time
print(f'Total time taken {end - start}')
print(f'results first item{results[0]}')
