import glob
import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from trading_app.utils import get_lean_data
from trading_app.database import get_db
from trading_app.models import (Stock, Strategy, Backtest, BacktestStatistics,
                                BacktestProfitLoss, BacktestOrders, BacktestCharts)
from trading_app.schemas import RunBacktestRequest, RunBacktestResponse

router = APIRouter(
    prefix="/backtest",
    tags=['Backtest']
)


# helper functions
# todo: move helper functions to a separate file after it's working well
# 1. Write backtest to db
def write_backtest_to_db(json_file: str, symbol: str, strategy_name: str, db: Session = Depends(get_db)):
    # Load the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Query the Stock and Strategy tables to get the stock_id and strategy_id
    stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    strategy = db.query(Strategy).filter(Strategy.name == strategy_name).first()

    if not stock or not strategy:
        raise ValueError("Invalid stock symbol or strategy name")

    # Create a new Backtest instance
    backtest = Backtest(
        stock_strategy_stock_id=stock.id,
        stock_strategy_strategy_id=strategy.id,
        timestamp=data['State']['StartTime']
    )

    # Add the Backtest instance to the session
    db.add(backtest)
    db.commit()

    # Extract the necessary data from the JSON file
    statistics = data['Statistics']
    runtime_statistics = data['RuntimeStatistics']
    profit_loss = data['ProfitLoss']
    orders = data['Orders']
    charts = data['Charts']

    # Create instances of the other models with the extracted data
    # Remove '%' and '$' signs and convert to appropriate numeric type
    statistics_data = {
        'total_trades': int(statistics['Total Trades']),
        'average_win': float(statistics['Average Win'].replace('%', '')) / 100,
        'average_loss': float(statistics['Average Loss'].replace('%', '')) / 100,
        'compounding_annual_return': float(statistics['Compounding Annual Return'].replace('%', '')) / 100,
        'drawdown': float(statistics['Drawdown'].replace('%', '')) / 100,
        'expectancy': float(statistics['Expectancy']),
        'net_profit': float(statistics['Net Profit'].replace('%', '')) / 100,
        'sharpe_ratio': float(statistics['Sharpe Ratio']),
        'sortino_ratio': float(statistics['Sortino Ratio']),
        'probabilistic_sharpe_ratio': float(statistics['Probabilistic Sharpe Ratio'].replace('%', '')) / 100,
        'loss_rate': float(statistics['Loss Rate'].replace('%', '')) / 100,
        'win_rate': float(statistics['Win Rate'].replace('%', '')) / 100,
        'profit_loss_ratio': float(statistics['Profit-Loss Ratio']),
        'alpha': float(statistics['Alpha']),
        'beta': float(statistics['Beta']),
        'annual_standard_deviation': float(statistics['Annual Standard Deviation']),
        'annual_variance': float(statistics['Annual Variance']),
        'information_ratio': float(statistics['Information Ratio']),
        'tracking_error': float(statistics['Tracking Error']),
        'treynor_ratio': float(statistics['Treynor Ratio']),
        'total_fees': float(statistics['Total Fees'].replace('$', '')),
        'estimated_strategy_capacity': float(statistics['Estimated Strategy Capacity'].replace('$', '')),
        'lowest_capacity_asset': statistics['Lowest Capacity Asset'],
        'portfolio_turnover': float(statistics['Portfolio Turnover'].replace('%', '')) / 100,
        'equity': float(runtime_statistics['Equity'].replace('$', '').replace(',', '')),
        'fees': float(runtime_statistics['Fees'].replace('$', '').replace(',', '')),
        'holdings': float(runtime_statistics['Holdings'].replace('$', '').replace(',', '')),
        'net_profit_runtime': float(runtime_statistics['Net Profit'].replace('$', '').replace(',', '')),
        'probabilistic_sharpe_ratio_runtime': float(
            runtime_statistics['Probabilistic Sharpe Ratio'].replace('%', '')) / 100,
        'return_runtime': float(runtime_statistics['Return'].replace(' %', '')) / 100,
        'unrealized': float(runtime_statistics['Unrealized'].replace('$', '').replace(',', '')),
        'volume': float(runtime_statistics['Volume'].replace('$', '').replace(',', ''))
    }

    statistic = BacktestStatistics(backtest_id=backtest.id, **statistics_data)
    db.add(statistic)

    for key, value in profit_loss.items():
        profit_loss_entry = BacktestProfitLoss(backtest_id=backtest.id, profit_loss_data=value)
        db.add(profit_loss_entry)

    for key, value in orders.items():
        order = BacktestOrders(backtest_id=backtest.id, order_data=value)
        db.add(order)

    for key, value in charts.items():
        chart = BacktestCharts(backtest_id=backtest.id, chart_data=value)
        db.add(chart)

    # Commit the session to save the changes to the database
    db.commit()


# 2. Get latest json file
def get_json_files(strategy_name):
    # Define the directory path for the strategy
    strategy_dir = os.path.join('strategy', strategy_name, 'backtests')

    # Get all directories under the strategy directory
    dirs = [d for d in os.listdir(strategy_dir) if os.path.isdir(os.path.join(strategy_dir, d))]
    # Sort the directories by date
    dirs.sort(key=lambda x: datetime.strptime(x, '%Y-%m-%d_%H-%M-%S'), reverse=True)
    # Get the newest directory
    newest_dir = dirs[0]
    # Use glob to find the JSON file that matches the pattern in the newest directory
    json_files = glob.glob(os.path.join(strategy_dir, newest_dir, '*.json'))
    # Define the pattern for the JSON file
    pattern = re.compile(r'\d{10}\.json$')
    # Filter the json_files list to only include files that match the pattern
    json_files = [f for f in json_files if pattern.match(os.path.basename(f))]
    # Since we know there's only one file that matches the pattern, we can just return the first item in the list
    return json_files[0]


@router.post('/run_backtest')
async def run_backtest(request: RunBacktestRequest, db: Session = Depends(get_db)):
    # 1. Run backtest
    symbol = request.symbol
    strategy = request.strategy

    # Ensure there's data for the selected symbol
    get_lean_data(tickers=[symbol], start_date='2022-01-01', end_date='2023-12-01')

    # Logic to modify the strategy script with the selected stock
    strategy_script_path = Path(f'strategy/{strategy}/main.py')

    # Read the original script
    try:
        with open(strategy_script_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Strategy script not found")

    # Modify the script content
    for i, line in enumerate(lines):
        if line.strip().startswith('self.symbol = self.AddData(IBData, '):
            # Preserve the original indentation
            indent = line[:len(line) - len(line.lstrip())]
            lines[i] = f'{indent}self.symbol = self.AddData(IBData, "{symbol}", Resolution.Daily).Symbol\n'
            break

    # Write the modified script back to the original file
    with open(strategy_script_path, 'w') as file:
        file.writelines(lines)

    # Run the backtest using subprocess
    process = subprocess.run(["lean", "backtest", f"strategy/{strategy}"], capture_output=True, text=True)

    if process.returncode != 0:
        raise HTTPException(status_code=500, detail="Backtest failed to start.")

    # 2. Save Results to DB
    # Get the JSON file
    json_file = get_json_files(strategy)

    # Write the backtest data to the database
    write_backtest_to_db(json_file, symbol, strategy, db)

    return RunBacktestResponse(message=f"Backtest for strategy '{strategy}' with symbol '{symbol}' initiated")
