from .database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    ForeignKey,
)

from sqlalchemy.orm import relationship


class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, nullable=False)
    company = Column(String, nullable=False)
    exchange = Column(String, nullable=False)

    # Define the relationship (optional, if you need to access StockPrice from Stock)
    stock_prices = relationship("StockPrice", back_populates="stock")


class StockPrice(Base):
    __tablename__ = 'stock_price'
    stock_id = Column(Integer, ForeignKey('stock.id'), primary_key=True)
    dt = Column(DateTime, primary_key=True, nullable=False)
    close = Column(Numeric(10, 4), nullable=False)
    high = Column(Numeric(10, 4), nullable=False)
    low = Column(Numeric(10, 4), nullable=False)
    trade_count = Column(Integer, nullable=False)
    open = Column(Numeric(10, 4), nullable=False)
    volume = Column(Numeric, nullable=False)
    vwap = Column(Numeric(10, 4), nullable=False)

    stock = relationship("Stock")


class Strategy(Base):
    __tablename__ = 'strategy'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class StockStrategy(Base):
    __tablename__ = 'stock_strategy'
    stock_id = Column(Integer, ForeignKey('stock.id'), primary_key=True)
    strategy_id = Column(Integer, ForeignKey('strategy.id'), primary_key=True)

    stock = relationship("Stock")
    strategy = relationship("Strategy")
