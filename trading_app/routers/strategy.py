from fastapi import HTTPException, Depends, APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from trading_app import models
from trading_app.database import get_db
from sqlalchemy.exc import IntegrityError
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/strategy",
    tags=['Strategy']
)

templates = Jinja2Templates(directory="templates")


