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
    strategies = relationship("StockStrategy", back_populates="stock", cascade="all, delete")


class StockPrice(Base):
    __tablename__ = 'stock_price'
    stock_id = Column(Integer, ForeignKey('stock.id', ondelete='CASCADE'), primary_key=True)
    dt = Column(DateTime, primary_key=True, nullable=False)
    close = Column(Numeric, nullable=False)
    high = Column(Numeric, nullable=False)
    low = Column(Numeric, nullable=False)
    open = Column(Numeric, nullable=False)
    volume = Column(BigInteger, nullable=False)
    # can be null as some stocks may not have 20 days of data
    sma20 = Column(Numeric, nullable=True)
    sma50 = Column(Numeric, nullable=True)
    rsi14 = Column(Numeric, nullable=True)
    stock = relationship("Stock", back_populates="stock_prices")


class Strategy(Base):
    __tablename__ = 'strategy'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Define the relationship (optional, if you need to access StockPrice from Stock)
    stocks = relationship("StockStrategy", back_populates="strategy", cascade="all, delete")


class StockStrategy(Base):
    __tablename__ = 'stock_strategy'
    stock_id = Column(Integer, ForeignKey('stock.id', ondelete='CASCADE'), primary_key=True)
    strategy_id = Column(Integer, ForeignKey('strategy.id', ondelete='CASCADE'), primary_key=True)

    stock = relationship("Stock", back_populates="strategies")
    strategy = relationship("Strategy", back_populates="stocks")
