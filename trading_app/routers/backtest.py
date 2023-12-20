import subprocess
from pathlib import Path

from fastapi import HTTPException, APIRouter, Depends, Request
from sqlalchemy.orm import Session

from trading_app.utils import get_lean_data
from trading_app.database import get_db
from trading_app.schemas import RunBacktestRequest, RunBacktestResponse
from trading_app.utils import get_json_files, write_backtest_to_db
from trading_app.models import Backtest, BacktestCharts, BacktestStatistics
from sqlalchemy.orm import joinedload

from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/backtest",
    tags=['Backtest']
)

templates = Jinja2Templates(directory="templates")


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


@router.get("/all_backtests")
def get_all_backtests(request: Request, db: Session = Depends(get_db)):
    # Query all backtests from the database and join with StockStrategy table
    backtests = db.query(Backtest).options(joinedload(Backtest.stock), joinedload(Backtest.strategy)).all()

    # Pass the backtests to the template
    return templates.TemplateResponse("backtests.html", {"request": request, "backtests": backtests})


@router.get("/backtest_charts/{backtest_id}/{variable_name}")
def get_backtest_charts(backtest_id: int, variable_name: str, db: Session = Depends(get_db)):
    # Query all BacktestCharts for the specified backtest and variable from the database
    charts = db.query(BacktestCharts).filter(BacktestCharts.backtest_id == backtest_id, BacktestCharts.variable_name == variable_name).all()

    # Convert the charts to a format suitable for the frontend
    charts_data = [{"timestamp": chart.timestamp, "value": chart.value} for chart in charts]

    return charts_data


@router.get("/backtest_statistics/{backtest_id}")
def get_backtest_statistics(backtest_id: int, db: Session = Depends(get_db)):
    # Query the BacktestStatistics for the specified backtest from the database
    statistics = db.query(BacktestStatistics).filter(BacktestStatistics.backtest_id == backtest_id).first()

    # Convert the statistics to a dictionary
    statistics_data = {column.name: getattr(statistics, column.name) for column in statistics.__table__.columns}

    return statistics_data