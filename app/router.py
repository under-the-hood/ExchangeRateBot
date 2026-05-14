from fastapi import APIRouter

from app.api import router


main_router = APIRouter()

main_router.include_router(router)