import alpaca_trade_api as tradeapi


# from config import settings
APCA_API_KEY_ID = "AK8VVA617A8S1ICHKD67"
APCA_API_SECRET_KEY = "O4jrYbarF7eePJB5VsWkX6fh4orePjtjur5pn46R"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(
    key_id=APCA_API_KEY_ID,
    secret_key=APCA_API_SECRET_KEY,
    api_version="v2",
)

# obtain account information
account = api.get_account()
print(account)
