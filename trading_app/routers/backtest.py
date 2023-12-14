from fastapi import HTTPException, APIRouter
import subprocess
from pathlib import Path
from trading_app.schemas import RunBacktestRequest, RunBacktestResponse

router = APIRouter(
    prefix="/backtest",
    tags=['Backtest']
)


@router.post('/run_backtest')
async def run_backtest(request: RunBacktestRequest):
    symbol = request.symbol
    strategy = request.strategy

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

    return RunBacktestResponse(message=f"Backtest for strategy '{strategy}' with symbol '{symbol}' initiated")
