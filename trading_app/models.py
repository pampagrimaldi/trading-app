from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    ForeignKey,
    Boolean,
    BigInteger,
    JSON
)


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


class Backtest(Base):
    __tablename__ = 'backtest'
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey('stock.id', ondelete='CASCADE'))
    strategy_id = Column(Integer, ForeignKey('strategy.id', ondelete='CASCADE'))
    timestamp = Column(DateTime, nullable=False)

    # Define the relationships
    statistics = relationship("BacktestStatistics", back_populates="backtest", cascade="all, delete")
    profit_loss = relationship("BacktestProfitLoss", back_populates="backtest", cascade="all, delete")
    orders = relationship("BacktestOrders", back_populates="backtest", cascade="all, delete")
    charts = relationship("BacktestCharts", back_populates="backtest", cascade="all, delete")

    stock = relationship("Stock")
    strategy = relationship("Strategy")


class BacktestStatistics(Base):
    __tablename__ = 'backtest_statistics'
    id = Column(Integer, primary_key=True, index=True)
    backtest_id = Column(Integer, ForeignKey('backtest.id', ondelete='CASCADE'))

    total_trades = Column(Integer, nullable=True)
    average_win = Column(Numeric, nullable=True)
    average_loss = Column(Numeric, nullable=True)
    compounding_annual_return = Column(Numeric, nullable=True)
    drawdown = Column(Numeric, nullable=True)
    expectancy = Column(Numeric, nullable=True)
    net_profit = Column(Numeric, nullable=True)
    sharpe_ratio = Column(Numeric, nullable=True)
    sortino_ratio = Column(Numeric, nullable=True)
    probabilistic_sharpe_ratio = Column(Numeric, nullable=True)
    loss_rate = Column(Numeric, nullable=True)
    win_rate = Column(Numeric, nullable=True)
    profit_loss_ratio = Column(Numeric, nullable=True)
    alpha = Column(Numeric, nullable=True)
    beta = Column(Numeric, nullable=True)
    annual_standard_deviation = Column(Numeric, nullable=True)
    annual_variance = Column(Numeric, nullable=True)
    information_ratio = Column(Numeric, nullable=True)
    tracking_error = Column(Numeric, nullable=True)
    treynor_ratio = Column(Numeric, nullable=True)
    total_fees = Column(Numeric, nullable=True)
    estimated_strategy_capacity = Column(Numeric, nullable=True)
    lowest_capacity_asset = Column(String)
    portfolio_turnover = Column(Numeric, nullable=True)
    equity = Column(Numeric, nullable=True)
    fees = Column(Numeric, nullable=True)
    holdings = Column(Numeric, nullable=True)
    net_profit_runtime = Column(Numeric, nullable=True)
    probabilistic_sharpe_ratio_runtime = Column(Numeric, nullable=True)
    return_runtime = Column(Numeric, nullable=True)
    unrealized = Column(Numeric, nullable=True)
    volume = Column(Numeric, nullable=True)

    backtest = relationship("Backtest", back_populates="statistics")


class BacktestProfitLoss(Base):
    __tablename__ = 'backtest_profit_loss'
    id = Column(Integer, primary_key=True, index=True)
    backtest_id = Column(Integer, ForeignKey('backtest.id', ondelete='CASCADE'))
    # profit_loss_data = Column(JSON, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    value = Column(Numeric, nullable=False)

    # Define the relationship
    backtest = relationship("Backtest", back_populates="profit_loss")


class BacktestOrders(Base):
    __tablename__ = 'backtest_orders'
    id = Column(Integer, primary_key=True, index=True)
    backtest_id = Column(Integer, ForeignKey('backtest.id', ondelete='CASCADE'))
    # order_data = Column(JSON, nullable=False)
    order_id = Column(Integer, nullable=True)
    order_type = Column(Integer, nullable=True)
    contingent_id = Column(Integer, nullable=True)
    broker_id = Column(String, nullable=True)
    symbol_value = Column(String, nullable=True)
    symbol_id = Column(String, nullable=True)
    symbol_permtick = Column(String, nullable=True)
    price = Column(Numeric, nullable=True)
    price_currency = Column(String, nullable=True)
    time = Column(DateTime, nullable=True)
    created_time = Column(DateTime, nullable=True)
    last_fill_time = Column(DateTime, nullable=True)
    quantity = Column(Numeric, nullable=True)
    status = Column(Integer, nullable=True)
    tag = Column(String, nullable=True)
    security_type = Column(Integer, nullable=True)
    direction = Column(Integer, nullable=True)
    value = Column(Numeric, nullable=True)
    bid_price = Column(Numeric, nullable=True)
    ask_price = Column(Numeric, nullable=True)
    last_price = Column(Numeric, nullable=True)
    is_marketable = Column(Boolean, nullable=True)
    price_adjustment_mode = Column(Integer, nullable=True)

    backtest = relationship("Backtest", back_populates="orders")


class BacktestCharts(Base):
    __tablename__ = 'backtest_charts'
    id = Column(Integer, primary_key=True, index=True)
    backtest_id = Column(Integer, ForeignKey('backtest.id', ondelete='CASCADE'))
    timestamp = Column(DateTime, nullable=False)
    variable_name = Column(String, nullable=False)
    value = Column(Numeric, nullable=False)

    backtest = relationship("Backtest", back_populates="charts")