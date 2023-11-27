import alpaca_trade_api as tradeapi
from trading_app.config import settings
from trading_app import models
from trading_app.database import get_db, SessionLocal
from sqlalchemy.orm import Session

# note this is the legacy version of the api - alpaca-py is the latest but can't get it to work
# version 1 working

# todo: check lean instead of alpaca
# todo: check timescaleDB instead of PG (try with psycopg2)
# todo: introduce RL algos


api = tradeapi.REST(
    key_id=settings.apca_key,
    secret_key=settings.apca_secret_key,
    api_version="v2",
)
