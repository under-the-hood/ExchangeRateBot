from httpx import AsyncClient
import asyncio
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select

from config import url, currency
from models.user import User
from database.database import new_session
from utils.bot_loader import bot


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


router = Router()

@router.message(Command("start"))
async def subscribe_user(message: Message):
    """
    Registers the user in the notification system if they are not already subscribed.
    """
    tg_user_id = message.from_user.id

    async with new_session() as session:
        stmt = (insert(User).values(user_id=tg_user_id).on_conflict_do_nothing(index_elements=['user_id']))

        await session.execute(stmt)
        await session.commit()

        await message.answer("You have successfully subscribed to exchange rate updates!")