from pydantic_settings import BaseSettings


# define the settings class
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    apca_key: str
    apca_secret_key: str
    apca_api_base_url: str
    polygon_key: str
    alphavantage_key: str
    ibeam_account: str
    ibeam_password: str
    quantconnect_token: str
    quantconnect_user: str
    coinbase_key: str
    coinbase_secret: str
    coinbase_pass: str
    binance_api_key: str
    binance_api_secret: str
    binance_password: str

    class Config:
        env_file = ".env"


# create an instance of the settings class
settings = Settings()
