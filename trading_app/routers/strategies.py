from fastapi import HTTPException, Depends, APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from trading_app.models import Stock, StockPrice, Strategy, StockStrategy
from trading_app.database import get_db
from sqlalchemy.exc import IntegrityError
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, and_
from typing import List, Dict

router = APIRouter(
    prefix="/strategies",
    tags=['Strategy']
)

templates = Jinja2Templates(directory="templates")


@router.get("/all_strategies")
def get_all_strategies(request: Request, db: Session = Depends(get_db)):





    return templates.TemplateResponse("strategies.html", {"request": request})
