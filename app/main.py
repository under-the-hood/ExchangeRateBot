import asyncio
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from app.services.services import track_rate_changes
from app.router import main_router
from app.utils.bot_loader import dp, bot
from app.handlers.handlers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    dp.include_router(router)
    asyncio.create_task(dp.start_polling(bot))
    monitoring_task = asyncio.create_task(track_rate_changes())
    yield
    monitoring_task.cancel()

app = FastAPI(lifespan=lifespan)
app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)