import alpaca_trade_api as tradeapi
from trading_app.config import settings
# version 1 working

# todo: check lean instead of alpaca
# todo: check timescaleDB instead of PG (try with psycopg2)
# todo: introduce RL algos
# todo: try psycopg3

api = tradeapi.REST(
    key_id=settings.apca_key,
    secret_key=settings.apca_secret_key,
    api_version="v2",
)
