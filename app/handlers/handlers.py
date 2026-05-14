from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message

from app.services.services import create_user


router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    tg_user_id = message.from_user.id
    await create_user(user_id=tg_user_id)
    await message.answer("You have successfully subscribed to exchange rate updates!")