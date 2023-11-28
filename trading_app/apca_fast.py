import psycopg2
from trading_app.config import settings
import pandas as pd
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
from trading_app.trader import api
from io import StringIO

# Connect to the database
conn = psycopg2.connect(f"host={settings.database_hostname} "
                       f"dbname={settings.database_name} "
                       f"user={settings.database_username} " 
                       f"password={settings.database_password}")


# Create a dataframe
barsets = api.get_bars(['AAPL'], TimeFrame.Day, "2023-11-23", adjustment="raw").df
barsets.reset_index(inplace=True)
barsets['timestamp'] = barsets['timestamp'].dt.tz_convert(None)


# Fetch the symbol to stock_id mapping
with conn.cursor() as cur:
    cur.execute("SELECT symbol, id FROM public.stock")
    symbol_to_stock_id = {symbol: stock_id for symbol, stock_id in cur.fetchall()}

# print("Symbol to stock_id mapping:", symbol_to_stock_id)  # Debug: Print the mapping

# Map 'symbol' to 'stock_id'
barsets['stock_id'] = barsets['symbol'].map(symbol_to_stock_id)

# Check for any NaN values in 'stock_id' after mapping
if barsets['stock_id'].isnull().any():
    print("Warning: Some 'stock_id' values are NaN")

# Select and reorder DataFrame columns to match the table schema
barsets = barsets[['stock_id', 'open', 'high', 'low',
                   'close', 'volume', 'vwap', 'timestamp', 'trade_count']]

# print(barsets.info())

# Initialize a string buffer
sio = StringIO()
sio.write(barsets.to_csv(index=None, header=None))  # Write the Pandas DataFrame as a csv to the buffer
sio.seek(0)  # Be sure to reset the position to the start of the stream


# Copy the string buffer to the database, as if it were an actual file
with conn.cursor() as c:
    try:
        c.copy_from(sio, "stock_price", columns=barsets.columns, sep=',')
        conn.commit()

    except Exception as e:
        print(e)
        conn.rollback()

