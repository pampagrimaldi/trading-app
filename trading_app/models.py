from .database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    ForeignKey,
    Boolean,
    BigInteger
)

from sqlalchemy.orm import relationship


class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    ib_symbol = Column(String, unique=True, nullable=False)
    symbol = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    asset_class = Column(String, nullable=False)
    conid = Column(Integer, unique=True, nullable=False)
    exchange = Column(String, nullable=False)
    is_us = Column(Boolean, nullable=False)

    # Define the relationship (optional, if you need to access StockPrice from Stock)
    stock_prices = relationship("StockPrice", back_populates="stock", cascade="all, delete")


class StockPrice(Base):
    __tablename__ = 'stock_price'
    stock_id = Column(Integer, ForeignKey('stock.id', ondelete='CASCADE'), primary_key=True)
    dt = Column(DateTime, primary_key=True, nullable=False)
    close = Column(Numeric(10, 4), nullable=False)
    high = Column(Numeric(10, 4), nullable=False)
    low = Column(Numeric(10, 4), nullable=False)
    trade_count = Column(BigInteger, nullable=False)
    open = Column(Numeric(10, 4), nullable=False)
    volume = Column(Numeric, nullable=False)

    stock = relationship("Stock", back_populates="stock_prices")


# class Strategy(Base):
#     __tablename__ = 'strategy'
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#
#
# class StockStrategy(Base):
#     __tablename__ = 'stock_strategy'
#     stock_id = Column(Integer, ForeignKey('stock.id'), primary_key=True)
#     strategy_id = Column(Integer, ForeignKey('strategy.id'), primary_key=True)
#
#     stock = relationship("Stock")
#     strategy = relationship("Strategy")
