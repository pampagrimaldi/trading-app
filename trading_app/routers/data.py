from fastapi import HTTPException, Depends, APIRouter, Request
from sqlalchemy.orm import Session
from trading_app import models
from trading_app.database import get_db
from sqlalchemy.exc import IntegrityError
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import joinedload

router = APIRouter(
    prefix="/data",
    tags=['Data']
)

templates = Jinja2Templates(directory="templates")


@router.get("/stock_table")
def get_all_stocks(request: Request, db: Session = Depends(get_db)):
    try:
        stocks = (db
                  .query(models.Stock)
                  .order_by(models.Stock.company.asc())
                  .all())

        template_response = (templates
                             .TemplateResponse("index.html",
                                               {"request": request, "stocks": stocks}))

        return template_response
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stock_table/{symbol}")
def get_stock(request: Request, symbol: str, db: Session = Depends(get_db)):
    try:
        stock = (db.query(models.Stock)
                 .options(joinedload(models.Stock.stock_prices))
                 .filter(models.Stock.symbol == symbol).first())

        if stock is None:
            raise HTTPException(status_code=404, detail="Stock not found")

        template_response = (templates
                             .TemplateResponse("stock_detail.html", {"request": request,
                                                                     "stock": stock}))

        return template_response
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))
