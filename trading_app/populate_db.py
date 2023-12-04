import alpaca_trade_api as tradeapi
from trading_app import models
from trading_app.database import SessionLocal
from trading_app.trader import api
from sqlalchemy.orm import Session
import logging
import os
from tqdm import tqdm

# Setup logging
script_dir = os.path.dirname(os.path.realpath(__file__))
project_root_dir = os.path.dirname(script_dir)  # Move one directory up to the project root
logs_dir = os.path.join(project_root_dir, "logs")

# Create logs directory if it doesn't exist
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

log_file_path = os.path.join(logs_dir, "trading_app.log")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)


# Function to insert stock data
def insert_stock_data(session: Session, symbol: str, company: str, exchange: str):
    existing_stock = session.query(models.Stock).filter(models.Stock.symbol == symbol).first()
    if not existing_stock:
        new_stock = models.Stock(symbol=symbol, company=company, exchange=exchange)
        session.add(new_stock)
        return True
    return False


try:
    # Fetch assets and limit to the first 1000
    all_assets = api.list_assets(asset_class="us_equity", status="active")
    filtered_assets = [asset for asset in all_assets if asset.tradable][:1000]

    new_stock_count = 0  # Initialize a counter for new stocks
    with SessionLocal() as session:
        for asset in tqdm(filtered_assets):
            if insert_stock_data(session, asset.symbol, asset.name, asset.exchange):
                new_stock_count += 1  # Increment counter for each new stock added

        session.commit()
        logger.info(f"{new_stock_count} new stocks were added to the database.")
        if new_stock_count == 0:
            logger.info("No new stocks were found to add.")

except Exception as e:
    logger.error(f"Error during script execution: {e}")
