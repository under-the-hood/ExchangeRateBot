from aiogram import Bot, Dispatcher

from config import settings
from services.services import router

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)