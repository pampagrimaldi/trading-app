# import FastAPI and other libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from .routers import topics, questions, suburbs, user, bulk, multiplayer, places


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


# test
@app.get("/")
def index():
    return {"message": "Welcome to Pampa's trading app backend"}