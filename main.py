import asyncio
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from services.services import track_rate_changes
from router import main_router
from utils.bot_loader import dp, bot


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(dp.start_polling(bot))
    monitoring_task = asyncio.create_task(track_rate_changes())
    yield
    monitoring_task.cancel()

app = FastAPI(lifespan=lifespan)
app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)