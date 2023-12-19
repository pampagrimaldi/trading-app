import streamlit as st
from sqlalchemy import text

# Create the SQL connection to your database as specified in your secrets file.
conn = st.connection('stock_db', type='sql')

# Your SQL query
sql_query = text("""
WITH MostRecentDate AS (
    SELECT stock_id, MAX(dt) AS most_recent_date
    FROM stock_price
    GROUP BY stock_id
)
SELECT s.ib_symbol, s.name, MostRecentDate.most_recent_date,
       round(sp.close,2)  AS "closing price", round(sp.sma20,2) as SMA20, round(sp.sma50,2) as SMA50, round(sp.rsi14,2) as RSI14
FROM stock as s
JOIN MostRecentDate ON s.id = MostRecentDate.stock_id
JOIN stock_price as sp ON sp.stock_id = s.id AND sp.dt = MostRecentDate.most_recent_date
ORDER BY s.name ASC;
""")

# Execute the SQL query with conn.session.
with conn.session as s:
    s.execute(sql_query)
    s.commit()

# Add a Title
st.title('Stock Price Dashboard')

# Query and display the data
data = conn.query(str(sql_query))
st.dataframe(data)