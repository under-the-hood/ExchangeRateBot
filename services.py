from httpx import AsyncClient
import asyncio

from config import url, currency, users_to_send, telegram_token


async def get_exchange_rate(url: str, currency: str):

    async with AsyncClient() as client:
        query_params = {
            'text': currency
        }
        
        resp = await client.get(url, params=query_params)

        if resp.status_code != 200:
            print('The request failed with an error', resp.text) 

        all_data = resp.json()
        target_currency = all_data["usd"][currency]

        return target_currency


async def track_rate_changes():
    last_rate = None

    while True:
        current_rate = await get_exchange_rate(url, currency)

        if current_rate:
            if current_rate != last_rate and last_rate is not None:
                async with AsyncClient() as client:
                    for user_id in users_to_send:
                        await client.post(
                                f"https://api.telegram.org/bot{telegram_token}/sendMessage",
                                data={
                                    "chat_id": user_id,
                                    "text": f"Exchange rate for {currency} was changed! Latest rate: {current_rate}"}
                                    )
            last_rate = current_rate
        await asyncio.sleep(3600)   # 1 hour


async def get_current_exchange_rate_service(current_currency: str = None):
    if not current_currency:
        current_currency = currency

    rate = await get_exchange_rate(url, current_currency)
    return rate