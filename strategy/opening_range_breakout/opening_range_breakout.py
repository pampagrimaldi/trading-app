from trading_app.database import SessionLocal
from trading_app.models import Strategy, StockStrategy, Stock


# get all stocks in the database based on strategy
def get_stocks(strategy_name: str):
    with SessionLocal() as session:
        try:
            # get strategy id
            strategy_id = session.query(Strategy).filter(
                Strategy.name == strategy_name).first().id

            # get all stocks based on strategy id
            stocks = (session
                      .query(Stock)
                      .join(StockStrategy,
                            Stock.id == StockStrategy.stock_id)
                      .filter(StockStrategy.strategy_id == strategy_id)
                      .all())

            # return ib symbols
            return [stock.ib_symbol for stock in stocks]
        except Exception as e:
            print(e)
            return None


if __name__ == '__main__':
    print(get_stocks('opening_range_breakout'))
