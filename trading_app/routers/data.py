from fastapi import HTTPException, Depends, APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from trading_app.models import Stock, StockPrice, Strategy, StockStrategy
from trading_app.database import get_db
from sqlalchemy.exc import IntegrityError
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, and_

router = APIRouter(
	prefix="/data",
	tags=['Data']
)

templates = Jinja2Templates(directory="templates")


@router.get("/stock_table")
def get_all_stocks(request: Request, db: Session = Depends(get_db)):
	stock_filter = request.query_params.get("filter", False)

	# Query the most recent date in the stock_price table and format it as a date
	most_recent_date = db.query(func.date(func.max(StockPrice.dt))).scalar()
	print(f"Most recent date being used for filtering: {most_recent_date}")

	if stock_filter in ['new_closing_highs', 'new_closing_lows']:
		# Determine whether to find max or min closing price
		price_func = func.max if stock_filter == 'new_closing_highs' else func.min
		price_label = 'max_close' if stock_filter == 'new_closing_highs' else 'min_close'

		# Define a CTE for the closing price (max or min based on filter)
		ClosingPrice = (db
						.query(StockPrice.stock_id, price_func(StockPrice.close).label(price_label))
						.group_by(StockPrice.stock_id)
						.cte('ClosingPrice'))

		# Construct the main query
		query = (db
				 .query(Stock.symbol, Stock.name, StockPrice.stock_id,
						getattr(ClosingPrice.c, price_label),
						StockPrice.dt)
				 .join(ClosingPrice, and_(StockPrice.stock_id == ClosingPrice.c.stock_id,
										  StockPrice.close == getattr(ClosingPrice.c, price_label)))
				 .join(Stock, Stock.id == StockPrice.stock_id)
				 .filter(func.date(StockPrice.dt) == most_recent_date)
				 .order_by(Stock.name.asc()))

		# Execute the query
		stocks = query.all()

	else:
		stocks = (db
				  .query(Stock)
				  .order_by(Stock.name.asc())
				  .all())

	try:

		template_response = (templates.TemplateResponse("index.html", {"request": request, "stocks": stocks}))

		return template_response
	except IntegrityError as e:
		raise HTTPException(status_code=400, detail=str(e))


@router.get("/stock_table/{symbol}")
def get_stock(request: Request, symbol: str, db: Session = Depends(get_db)):
	try:
		# Query the Stock table
		stock = (db
				 .query(Stock)
				 .filter(Stock.symbol == symbol)
				 .first())

		# Strategies
		strategies = db.query(Strategy).all()

		if stock is None:
			raise HTTPException(status_code=404, detail="Stock not found")

		# Query the StockPrice table separately, ordering by 'dt'
		stock_prices = (db.query(StockPrice)
						.filter(StockPrice.stock_id == stock.id)
						.order_by(StockPrice.dt.desc())
						.all())

		template_response = templates.TemplateResponse("stock_detail.html",
													   {"request": request,
														"stock": stock,
														"stock_prices": stock_prices,
														"strategies": strategies})

		return template_response
	except IntegrityError as e:
		raise HTTPException(status_code=400, detail=str(e))


@router.post("/stock_table/apply_strategy")
def apply_strategy(stock_id: int = Form(...), strategy_id: int = Form(...), db: Session = Depends(get_db)):
	# insert into the stock_strategy table
	try:
		# Create the StockStrategy object
		stock_strategy = StockStrategy(stock_id=stock_id, strategy_id=strategy_id)
		# Add the StockStrategy object to the session
		db.add(stock_strategy)
		db.commit()
		# Redirect to the stock detail page for the stock that was just updated
		return RedirectResponse(url=f"/data/stock_table/strategy/{strategy_id}", status_code=303)
	except IntegrityError as e:
		# show more details on error
		raise HTTPException(status_code=400, detail=str(e))


@router.get("/stock_table/strategy/{strategy_id}")
def get_strategy(request: Request, strategy_id: int, db: Session = Depends(get_db)):
	try:
		# Get the strategy
		strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()

		if strategy is None:
			raise HTTPException(status_code=404, detail="Strategy not found")

		# Join Stock and StockStrategy tables
		stocks = (db
				  .query(Stock)
				  .join(StockStrategy, Stock.id == StockStrategy.stock_id)
				  .filter(StockStrategy.strategy_id == strategy_id)
				  .all())

		# Render the template with strategy and associated stocks
		template_response = templates.TemplateResponse("strategy_detail.html",
													   {"request": request,
														"strategy": strategy,
														"stocks": stocks})
		return template_response
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))
