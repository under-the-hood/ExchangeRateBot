import asyncio

from app.services.rate import track_rate_changes
from app.utils.bot_loader import dp, bot
from app.handlers.handlers import router
from app.middlewares.user import check_user_registration


async def main():
    # 1. Connect middlewares
    dp.message.middleware(check_user_registration)
    
    # 2. Conneсt router
    dp.include_router(router)
    
    # 3. Start monitoring in background mode
    asyncio.create_task(track_rate_changes())
    
    # 4. Start bot
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())