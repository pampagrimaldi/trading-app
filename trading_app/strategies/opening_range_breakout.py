from datetime import datetime, timedelta
from trading_app import models
from trading_app.database import SessionLocal
from trading_app.trader import api
from alpaca_trade_api.rest import TimeFrame
from sqlalchemy.orm import Session


def opening_range_breakout(session: Session, strategy: str):

	# Query the strategy ID
	strategy_record = (session
					   .query(models.Strategy)
					   .filter(models.Strategy.name == strategy)
					   .first())

	if strategy_record is None:
		raise ValueError("Strategy not found")

	strategy_id = strategy_record.id

	# Efficiently join and filter stocks related to the strategy
	stocks = (session
			  .query(models.Stock.symbol, models.Stock.company)
			  .join(models.StockStrategy, models.StockStrategy.stock_id == models.Stock.id)
			  .filter(models.StockStrategy.strategy_id == strategy_id)
			  .all())

	symbols = [stock.symbol for stock in stocks]
	# fetch data with alpaca api
	# todo: it's delta -1 as its based on US (Change when using Aussie stocks)
	start_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
	bars = api.get_bars(symbols, TimeFrame.Minute, start_date, adjustment="raw").df
	print('=== bars head ===')
	print(bars.head())


# Example usage
try:
	with SessionLocal() as session:
		opening_range_breakout(session, 'opening_range_breakout')
except Exception as e:
	print(e)

