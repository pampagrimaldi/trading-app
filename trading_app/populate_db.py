import alpaca_trade_api as tradeapi
from trading_app import models
from trading_app.database import get_db, SessionLocal
from trading_app.trader import api
from sqlalchemy.orm import Session


# note this is the legacy version of the api - alpaca-py is the latest but can't get it to work
# version 1 working

# todo: check lean instead of alpaca
# todo: check timescaleDB instead of PG (try with psycopg2)
# todo: introduce RL algos


# check assets
assets = api.list_assets()


# Function to insert stock data
def insert_stock_data(session: Session, symbol: str, company: str):
    # Check if the stock already exists
    existing_stock = (
        session.query(models.Stock).filter(models.Stock.symbol == symbol).first()
    )

    if not existing_stock:
        new_stock = models.Stock(symbol=symbol, company=company)
        session.add(new_stock)


# Create a database session and insert data
with SessionLocal() as session:
    for asset in assets:
        try:
            if asset.status == "active" and asset.tradable:
                # Insert stock data if not already present
                insert_stock_data(session, asset.symbol, asset.name)
        except Exception as e:
            print(f"Error processing asset {asset.symbol}: {e}")

    # Commit the session to save changes
    session.commit()
