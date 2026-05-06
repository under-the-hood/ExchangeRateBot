import os
from dotenv import load_dotenv

load_dotenv()
url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json"
currency = "rub"    #Set your currency
telegram_token = os.getenv("BOT_TOKEN")

users_to_send = [
    ...     #set your telegram id
]