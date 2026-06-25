from redis import asyncio

from app.config import settings


redis = asyncio.from_url(
    url=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    decode_responses=True
)