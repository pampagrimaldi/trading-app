import psycopg2
from trading_app.config import settings
from trading_app import models
from alpaca_trade_api.rest import TimeFrame
from trading_app.trader import api
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from io import StringIO
import time  # Make sure to import the time module
import time
import logging
import os
from tqdm import tqdm
import pandas as pd

# Connect to the database
conn = psycopg2.connect(f"host={settings.database_hostname} "
                        f"dbname={settings.database_name} "
                        f"user={settings.database_username} "
                        f"password={settings.database_password}")

# Setup logging
def setup_logging():
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    log_file_path = os.path.join(logs_dir, "stock_price_update.log")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(file_handler)
    return logger


logger = setup_logging()


def get_latest_data_date(session):
    """
    Returns the latest date for which data is available.
    If no data is found, returns None.
    """
    latest_data = ((session
                    .query(models.StockPrice)
                    .join(models.Stock)
                    .order_by(models.StockPrice.timestamp.desc()).first()))

    return latest_data.timestamp if latest_data else None


# Function to fetch and insert stock prices
def fetch_and_insert_stock_prices(session: Session, symbols: list):
    with conn.cursor() as cur:
        cur.execute("SELECT symbol, id FROM public.stock")
        symbol_to_stock_id = {symbol: stock_id for symbol, stock_id in cur.fetchall()}

    start_str = (datetime.now() - timedelta(days=365 * 2)).strftime('%Y-%m-%d')  # Two years ago

    chunk_size = 200
    for i in tqdm(range(0, len(symbols), chunk_size)):
        chunk_symbols = symbols[i:i + chunk_size]

        # Measure API fetching time
        start_time_api = time.time()
        barsets = api.get_bars(chunk_symbols, TimeFrame.Day, start_str, adjustment="raw").df
        end_time_api = time.time()
        api_fetch_duration = end_time_api - start_time_api
        logger.info(f"API fetching time for chunk {i}: {api_fetch_duration} seconds")

        # barsets.reset_index(inplace=True)
        barsets['dt'] = pd.to_datetime(barsets.index).tz_convert(None)
        barsets['stock_id'] = barsets['symbol'].map(symbol_to_stock_id)

        if barsets['stock_id'].isnull().any():
            logger.warning("Some 'stock_id' values are NaN")

        barsets = barsets[['stock_id', 'dt', 'close',
                           'high', 'low', 'trade_count', 'open', 'volume', 'vwap']]

        print(barsets.info())

        sio = StringIO()
        sio.write(barsets.to_csv(index=None, header=None))
        sio.seek(0)

        # Measure database writing time
        start_time_db = time.time()
        with conn.cursor() as c:
            try:
                c.copy_from(sio, "stock_price", columns=barsets.columns, sep=',')
                conn.commit()
            except Exception as e:
                logger.error(e)
                conn.rollback()
        end_time_db = time.time()
        db_write_duration = end_time_db - start_time_db
        logger.info(f"Database writing time for chunk {i}: {db_write_duration} seconds")


if __name__ == "__main__":
    # get symbols list with psycopg2
    with conn.cursor() as cur:
        cur.execute("SELECT symbol FROM public.stock LIMIT 1000")
        symbols = [symbol for symbol, in cur.fetchall()]

    # Create a SQLAlchemy session
    with Session() as session:
        # Fetch and insert stock prices
        fetch_and_insert_stock_prices(session, symbols)
