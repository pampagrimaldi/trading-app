from pydantic import BaseModel


class RunBacktestRequest(BaseModel):
    symbol: str
    strategy: str


class RunBacktestResponse(BaseModel):
    message: str
