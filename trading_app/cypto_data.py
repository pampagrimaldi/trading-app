import ccxt
from trading_app.config import settings

ex = ccxt.binance({
    'enableRateLimit': True,
    'apiKey': settings.binance_api_key,
    'secret': settings.binance_api_secret,
})


# print(ex.fetch_balance())

ohlcv = ex.fetch_ohlcv('BTC/USDT', timeframe='1m',limit=500)

print(len(ohlcv))
