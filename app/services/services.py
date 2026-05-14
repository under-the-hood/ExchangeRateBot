from httpx import AsyncClient
import asyncio
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select

from app.config import url, currency
from app.models.user import User
from app.database.database import new_session
from app.utils.bot_loader import bot


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


async def get_all_users():
    async with new_session() as session:
        result = await session.execute(select(User.user_id))
        return result.scalars().all()

async def track_rate_changes():
    last_rate = None

    while True:
        current_rate = await get_exchange_rate(url, currency)

        if current_rate:
            if current_rate != last_rate and last_rate is not None:
                    for user_id in await get_all_users():
                        await bot.send_message(
                            chat_id=user_id,
                            text=f"Exchange rate for {currency} was changed! Latest rate: {current_rate}"
                        )
            last_rate = current_rate
        await asyncio.sleep(3600)   # 1 hour


async def get_current_exchange_rate_service(current_currency: str = None):
    if not current_currency:
        current_currency = currency

    rate = await get_exchange_rate(url, current_currency)
    return rate


async def create_user(tg_user_id: int):

    async with new_session() as session:
        stmt = (insert(User).values(user_id=tg_user_id).on_conflict_do_nothing(index_elements=['user_id']))

        await session.execute(stmt)
        await session.commit()