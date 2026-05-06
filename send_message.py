import requests

from config import users_to_send, currency, url, telegram_token
from utils import get_exchange_rate

async def send_message():
    for user_id in users_to_send:
        requests.post(
                        f"https://api.telegram.org/bot{telegram_token}/sendMessage",
                        data={
                            "chat_id": user_id,
                            "text": f"Exchange rate for {currency}: {get_exchange_rate(url, currency)}"}
                            )