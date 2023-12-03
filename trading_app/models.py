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


class StockPrice(Base):
    __tablename__ = 'stock_price'
    stock_id = Column(Integer, ForeignKey('stock.id'), primary_key=True)
    dt = Column(DateTime, primary_key=True, nullable=False)
    open = Column(Numeric(6, 2), nullable=False)
    high = Column(Numeric(6, 2), nullable=False)
    low = Column(Numeric(6, 2), nullable=False)
    close = Column(Numeric(6, 2), nullable=False)
    volume = Column(Numeric, nullable=False)
    # vwap = Column(Numeric(6, 2), nullable=False)
    # transactions = Column(Integer, nullable=False)

    # Define the relationship (optional, if you need to access Stock from StockPrice)
    stock = relationship("Stock")