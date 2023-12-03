import logging
import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from trading_app import models
from trading_app.database import SessionLocal
from polygon import RESTClient
from trading_app.config import settings


# Setup logging
def setup_logging():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_root_dir = os.path.dirname(script_dir)
    logs_dir = os.path.join(project_root_dir, "logs")

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    log_file_path = os.path.join(logs_dir, "stock_price_update.log")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(file_handler)
    return logger


logger = setup_logging()


# Function to fetch and insert stock prices
def fetch_and_insert_stock_prices(session: Session, stock: models.Stock, client: RESTClient):
    # Define your time range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)  # Corrected usage of timedelta
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    try:
        aggs = client.list_aggs(
            stock.symbol,
            1,
            "daily",
            start_str,
            end_str,
            limit=50000
        )

        for agg in aggs:
            stock_price = models.StockPrice(
                stock_id=stock.id,
                open=agg.open,
                high=agg.high,
                low=agg.low,
                close=agg.close,
                volume=agg.volume,
                vwap=agg.vwap,
                timestamp=datetime.fromtimestamp(agg.timestamp / 1000),  # Convert to datetime
                transactions=agg.transactions,
                otc=agg.otc
            )
            session.add(stock_price)

        session.commit()

    except Exception as e:
        logger.error(f"Error fetching or inserting data for {stock.symbol}: {e}")


def main():
    client = RESTClient(api_key=settings.polygon_key)

    try:
        with SessionLocal() as session:
            stocks = session.query(models.Stock).all()
            for stock in stocks:
                fetch_and_insert_stock_prices(session, stock, client)
        logger.info("Stock price update completed successfully.")

    except Exception as e:
        logger.error(f"Error in main script: {e}")


if __name__ == "__main__":
    main()
