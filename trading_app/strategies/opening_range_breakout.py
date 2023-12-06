from datetime import datetime, timedelta, date
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
	current_date = (date.today() - timedelta(days=1)).isoformat()
	print(f'current date {current_date}')
	start_minute_bar = f'{current_date}T13:30:00Z'  # For daylight saving time
	end_minute_bar = f'{current_date}T13:45:00Z'
	bars = api.get_bars(symbols, TimeFrame.Minute, current_date, adjustment="raw").df

	# masks
	opening_range_mask = (bars.index >= start_minute_bar) & (bars.index < end_minute_bar)
	# print first 10 items of symbol GDDY sort ascending on index
	print('\t'*4 + '======== first 20 items GDDY ========')
	print(bars[bars.symbol == 'GDDY'].head(20))
	# print open range mask
	print('\t'*4 + '======== opening range mask ========')
	print(bars[opening_range_mask])


# Example usage
try:
	with SessionLocal() as session:
		opening_range_breakout(session, 'opening_range_breakout')
except Exception as e:
	print(e)

