from typing import Callable, Dict
from aiogram.types import Message

from app.services.user import create_user
from app.database.redis_database import redis
from app.utils.cache import get_cache_key


async def check_user_registration(handler: Callable, event: Message, data: Dict):
    if event.from_user:
        tg_user_id = event.from_user.id

        redis_key = get_cache_key("user", "registered", tg_user_id)
        in_cache = await redis.get(redis_key)

        if in_cache:
            data["is_new_user"] = False
            await redis.expire(redis_key, 259200)   #3 days
        else:
            await create_user(tg_user_id=tg_user_id)
            await redis.set(redis_key, "1", 259200)
            data["is_new_user"] = True

        return await handler(event, data)