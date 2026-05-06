import asyncio

from send_message import send_message
from config import telegram_token

print(f"Token: {telegram_token}")

if __name__ == '__main__':
    asyncio.run(send_message())