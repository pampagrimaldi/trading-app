from .database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    BigInteger,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship


class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, nullable=False)
    company = Column(String, nullable=False)

    # Define the relationship (optional, if you need to access StockPrice from Stock)
    stock_prices = relationship("StockPrice", back_populates="stock")


class StockPrice(Base):
    __tablename__ = 'stock_price'
    stock_id = Column(Integer, ForeignKey('stock.id'), primary_key=True)
    dt = Column(DateTime, primary_key=True, nullable=False)
    close = Column(Numeric(10, 4), nullable=False)   # Adjusted precision and scale
    high = Column(Numeric(10, 4), nullable=False)    # Adjusted precision and scale
    low = Column(Numeric(10, 4), nullable=False)     # Adjusted precision and scale
    trade_count = Column(Integer, nullable=False)    # New column for trade count
    open = Column(Numeric(10, 4), nullable=False)    # Adjusted precision and scale
    volume = Column(Numeric, nullable=False)
    vwap = Column(Numeric(10, 4), nullable=False)    # New column for VWAP

    # Define the relationship (optional, if you need to access Stock from StockPrice)
    stock = relationship("Stock")