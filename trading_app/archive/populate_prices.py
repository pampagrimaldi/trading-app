import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
from trading_app import models
from trading_app.database import get_db, SessionLocal
from trading_app.trader import api
from sqlalchemy.orm import Session
import logging
import os


barsets = api.get_bars(["AAPL","MSFT"], TimeFrame.Minute,
                       "2021-06-08", "2021-06-08",
                       adjustment="raw").df

print("---- barsets info ----")
print(barsets.info())
print("---- barsets head ----")
print(barsets.head())
