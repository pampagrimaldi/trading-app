from .database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    BigInteger,
    ForeignKey,
    Boolean,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship


class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, nullable=False)
    company = Column(String, nullable=False)


# note: polygon aggregate return format Agg(open=178.26, high=178.26, low=178.21, close=178.21, volume=1118,
# vwap=178.2357, timestamp=1641200400000, transactions=65, otc=None)

class StockPrice(Base):
    __tablename__ = "stock_price"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stock.id"), nullable=False)
    open = Column(Numeric, nullable=False)
    high = Column(Numeric, nullable=False)
    low = Column(Numeric, nullable=False)
    close = Column(Numeric, nullable=False)
    volume = Column(BigInteger, nullable=False)
    vwap = Column(Numeric, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    trade_count = Column(Integer, nullable=False)

    stock = relationship("Stock")
