

Docker connection based on settings:

```yaml
version: '3.11.5'  
  
services:  
  sql:  
    image: postgres:16.1  
    container_name: postgres  
    environment:  
      - POSTGRES_PASSWORD=password  
      - POSTGRES_USER=trader  
      - POSTGRES_DB=stock_db  
    ports:  
      - "5432:5432"  
    volumes:  
      - stock_db:/var/lib/postgresql/data  
    restart: unless-stopped  
  
volumes:  
  stock_db:  
  
#  docker exec -it postgres psql -U trader -d stock_db
```

```zsh
docker exec -it postgres psql -U trader -d stock_db
```


## 1 Alpaca Emergency Code

```zsh
82e82fa5-df75-4944-bb43-702eacdda5a2
```


## 2 Scheduling

Crontabs are system wide methods, so this could be setup in the linux VM later.

To access it:
```zsh
crontab -e
```

For my own mac, the cron task to populate the stocks will be :

```
30 16 * * * cd /Users/pampagrimaldi/Documents/Projects/trading-app && /Users/pampagrimaldi/miniconda3/bin/poetry run python -m trading_app.populate_db
```


## 3 FastAPI

To start uvicorn

```
uvicorn trading_app.main:app --reload
```

## 4 SQL

find max close on each stock:

```sql
WITH MaxClosePrice AS (  
    SELECT sp.stock_id,  
           MAX(sp.close) AS max_close  
    FROM stock_price sp  
    GROUP BY sp.stock_id  
)  
SELECT s.symbol,  
       s.company,  
       sp.stock_id,  
       mcp.max_close,  
       sp.dt  
FROM stock_price sp  
JOIN MaxClosePrice mcp ON sp.stock_id = mcp.stock_id AND sp.close = mcp.max_close  
JOIN stock s ON sp.stock_id = s.id  
WHERE DATE(sp.dt) = '2023-12-01'  
ORDER BY s.company ASC;
```

Which is equivalent to the below in SQLAlchemy
```python
# Define a CTE for the maximum close price  
MaxClosePrice = (  
    db.query(  
        models.StockPrice.stock_id,  
        func.max(models.StockPrice.close).label('max_close')  
    )  
    .group_by(models.StockPrice.stock_id)  
    .cte('MaxClosePrice')  
)  
  
# Query the most recent date in the stock_price table and format it as a date  
most_recent_date = db.query(func.date(func.max(models.StockPrice.dt))).scalar()  
print(f"Most recent date being used for filtering: {most_recent_date}")  
  
# Construct the main query  
query = (  
    db.query(  
        models.Stock.symbol,  
        models.Stock.company,  
        models.StockPrice.stock_id,  
        MaxClosePrice.c.max_close,  
        models.StockPrice.dt  
    )  
    .join(MaxClosePrice, and_(  
        models.StockPrice.stock_id == MaxClosePrice.c.stock_id,  
        models.StockPrice.close == MaxClosePrice.c.max_close  
    ))  
    .join(models.Stock, models.Stock.id == models.StockPrice.stock_id)  
    .filter(func.date(models.StockPrice.dt) == most_recent_date)  
    .order_by(models.Stock.company.asc())  
)  
  
# Execute the query  
stocks = query.all()
```

## 5 Quantconnect

To push a project to the cloud:
```zsh
lean cloud push --project strategy/trade-spy    
```

Also, remember to run pull to update the docker images
```zsh
docker-compose pull
```


## 6 Todo

### 6.1 Data Sources

At the moment the project’s 

- [ ] The project has been runnign


### 6.2 User Interface

### 6.3 Modelling

### 6.4 Backtest Engine

### 6.5 Integration

### 6.6 Deployment

