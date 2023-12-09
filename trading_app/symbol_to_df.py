import pandas as pd
from pathlib import Path
from datetime import timedelta
from trading_app.database import SessionLocal
from trading_app.models import StockPrice, Stock

data_folder = './data'
ib_folder = './ibdata'


def get_stock_data(symbol: str, start_date, end_date):
    with SessionLocal() as session:
        stock_id = session.query(Stock).filter(Stock.symbol == symbol).first().id

        query = (session
                 .query(StockPrice.dt, StockPrice.open, StockPrice.high, StockPrice.low,
                        StockPrice.close, StockPrice.volume)
                 .filter(StockPrice.stock_id == stock_id,
                         StockPrice.dt >= start_date,
                         StockPrice.dt <= end_date)
                 .order_by(StockPrice.dt))

        df = pd.read_sql(query.statement, session.bind)
        df['dt'] = df['dt'].dt.strftime('%Y-%m-%d')  # Format the 'dt' column to date only
        df.rename(columns={'dt': None}, inplace=True)  # Remove the name of the 'dt' column
        df['volume'] = df['volume'].astype(int)  # Cast volume to integer

        # Format numeric columns to have exactly 14 decimal places
        for column in ['open', 'high', 'low', 'close']:
            df[column] = df[column].apply(lambda x: format(x, '.14f'))

        # Round numeric columns to 14 decimal places
        df['adjclose'] = df['close']
        df['ticker'] = symbol
        df = df[[None, 'open', 'high', 'low', 'close', 'adjclose', 'volume', 'ticker']]
        return df


def save_to_csv(df, symbol, folder):
    file_name = symbol.lower() + '.csv'
    path = Path(folder) / file_name
    df.to_csv(path, index=False)
    print(f'Saved data for {symbol} to {path}')


def get_lean_data(tickers: list, start_date, end_date):
    tickers = tickers if isinstance(tickers, list) else [tickers]
    folder = Path(data_folder) / ib_folder

    if not folder.exists():
        folder.mkdir()
        print(f'Folder {str(folder)} - Created')
    else:
        print(f'Folder {str(folder)} - Ok')

    loaded_tickers = []
    for ticker in tickers:
        try:
            df = get_stock_data(ticker, start_date, end_date)
            if not df.empty:
                save_to_csv(df, ticker, folder)
                loaded_tickers.append(ticker)
            else:
                print(f'No data available for {ticker}')
        except Exception as e:
            print(f'Problem getting data for ticker {ticker}: {e}')

    return loaded_tickers


if __name__ == '__main__':
    get_lean_data(['BHP', 'A2M'], '2022-01-01', '2023-12-01')