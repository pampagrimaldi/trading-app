import alpaca_trade_api as tradeapi
from trading_app import models
from trading_app.database import get_db, SessionLocal
from trading_app.trader import api
from sqlalchemy.orm import Session
import logging
import os
from tqdm import tqdm

# Setup logging
script_dir = os.path.dirname(os.path.realpath(__file__))
project_root_dir = os.path.dirname(
    script_dir
)  # Move one directory up to the project root
logs_dir = os.path.join(project_root_dir, "logs")

# Create logs directory if it doesn't exist
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

log_file_path = os.path.join(logs_dir, "trading_app.log")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)


# Function to insert stock data
def insert_stock_data(session: Session, symbol: str, company: str, exchange: str, new_stock_added):
    existing_stock = (session
                      .query(models.Stock)
                      .filter(models.Stock.symbol == symbol)
                      .first())

    if not existing_stock:
        new_stock = models.Stock(symbol=symbol, company=company,exchange=exchange)
        session.add(new_stock)
        logger.info(f"Added new stock: {symbol}, {company}")
        new_stock_added.append(True)


try:
    # Fetch assets and limit to the first 2000
    all_assets = api.list_assets(asset_class="us_equity",
                                 status="active")

    filtered_assets = [asset for asset in all_assets if asset.tradable][:1000]

    new_stock_added = []  # List to track if new stocks are added
    with SessionLocal() as session:
        for asset in tqdm(filtered_assets):
            insert_stock_data(session, asset.symbol, asset.name,asset.exchange, new_stock_added)

        session.commit()
        logger.info("Database update completed successfully.")

    if not new_stock_added:
        logger.info("No new stocks were found to add.")

except Exception as e:
    logger.error(f"Error during script execution: {e}")