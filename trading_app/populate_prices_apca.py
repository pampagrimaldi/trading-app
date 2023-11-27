import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
from trading_app import models
from trading_app.database import SessionLocal
from sqlalchemy.orm import Session
import logging
import os
from datetime import datetime, timedelta
from trading_app.trader import api
from tqdm import tqdm


# Setup logging
def setup_logging():
    logs_dir = "path_to_logs_directory"
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


def get_all_stock_symbols(session):
    """
    Fetches all stock symbols from the database.
    """
    return [stock.symbol for stock in session.query(models.Stock).all()]


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
    # Map symbols to their IDs in one query
    symbols_to_ids = {symbol: id for id, symbol in session.query(models.Stock.id, models.Stock.symbol)}

    start_str = (datetime.now() - timedelta(days=365 * 2)).strftime('%Y-%m-%d')  # Two years ago


    chunk_size = 200
    for i in tqdm(range(0, len(symbols), chunk_size)):
        chunk_symbols = symbols[i:i + chunk_size]

        try:
            barsets = api.get_bars(chunk_symbols, TimeFrame.Day, start_str, adjustment="raw")

            # Organize data by symbol
            bars_by_symbol = {symbol: [] for symbol in chunk_symbols}
            for bar in barsets:
                bars_by_symbol[bar['S']].append(bar)

            # Prepare data for bulk insert
            stock_prices = []
            for symbol, bars in bars_by_symbol.items():
                stock_id = symbols_to_ids.get(symbol)
                if stock_id:  # Ensure the stock symbol exists in the database
                    for bar in bars:
                        stock_price = models.StockPrice(
                            stock_id=stock_id,
                            open=bar['o'],
                            high=bar['h'],
                            low=bar['l'],
                            close=bar['c'],
                            volume=bar['v'],
                            vwap=bar['vw'],
                            timestamp=datetime.fromisoformat(bar['t']),
                            trade_count=bar['n']
                        )
                        stock_prices.append(stock_price)

            # Bulk insert
            session.bulk_save_objects(stock_prices)
            session.commit()
        except Exception as e:
            logger.error(f"Error in chunk starting at index {i}: {e}")
            session.rollback()

def main():
    try:
        with SessionLocal() as session:
            symbols = get_all_stock_symbols(session)  # Fetch stock symbols from the database
            fetch_and_insert_stock_prices(session, symbols)
        logger.info("Stock price update completed successfully.")
    except Exception as e:
        logger.error(f"Error in main script: {e}")


if __name__ == "__main__":
    main()
