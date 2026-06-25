from aiogram import Router
from aiogram.types import Message


router = Router()

@router.message()
async def subscribe_to_the_bot(message: Message, is_new_user: bool):
    if is_new_user:
        await message.answer("You have successfully subscribed to exchange rate updates!")
    else:
        await message.answer("New bot features will be added in the future")