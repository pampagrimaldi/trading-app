import time
import requests
from trading_app.config import settings

url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol={}&apikey={}'

symbols = ['AAPL', 'GOOG', 'TSLA', 'MSFT',
           'AAPL', 'GOOG', 'TSLA', 'MSFT',
           'AAPL', 'GOOG', 'TSLA', 'MSFT',
           'AAPL', 'GOOG', 'TSLA', 'MSFT',
           'AAPL', 'GOOG', 'TSLA', 'MSFT',
           'AAPL', 'GOOG', 'TSLA', 'MSFT']

results = []

# start time
start = time.time()

# create loop to fetch each symbols synchronously
for symbol in symbols:
    print(f'Working on symbol {symbol}')
    response = requests.get(url.format(symbol, settings.alphavantage_key))
    results.append(response.json())
print('Yoy did it!')

# end time
end = time.time()
print(f'Total time taken {end - start}')
