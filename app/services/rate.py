from httpx import AsyncClient
import asyncio

from app.config import url, currency
from app.utils.bot_loader import bot
from app.services.user import get_all_users


async def get_exchange_rate(url: str, currency: str):

    async with AsyncClient() as client:
        query_params = {
            'text': currency
        }
        
        resp = await client.get(url, params=query_params)

        if resp.status_code != 200:
            print('The request failed with an error', resp.text) 
            return None

        all_data = resp.json()
        target_currency = all_data["usd"][currency]

        return target_currency


async def track_rate_changes():
    last_rate = None

    while True:
        import random
        current_rate = random.random()
        #current_rate = await get_exchange_rate(url, currency)

        if current_rate:
            if current_rate != last_rate and last_rate is not None:
                    for user_id in await get_all_users():
                        await bot.send_message(
                            chat_id=user_id,
                            text=f"Exchange rate for {currency} was changed! Latest rate: {current_rate}"
                        )
            last_rate = current_rate
        await asyncio.sleep(1)   # 1 hour


#Will be used in the next commit
async def get_current_exchange_rate_service(current_currency: str = None):
    if not current_currency:
        current_currency = currency

    rate = await get_exchange_rate(url, current_currency)
    return rate