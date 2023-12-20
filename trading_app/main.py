# import FastAPI and other libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import data, backtest, strategies

# create FastAPI instance
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(auth.router)
app.include_router(data.router)
app.include_router(backtest.router)
app.include_router(strategies.router)


# test
@app.get("/")
def index():
    return {"message": "Welcome to Pampa's trading app backend"}