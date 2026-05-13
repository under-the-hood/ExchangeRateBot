from fastapi import APIRouter

from services.services import get_current_exchange_rate_service


router = APIRouter()

@router.get("/exchange_rates/get_exchange_rate")
async def get_current_exchange_rate(current_currency: str = None):
    return await get_current_exchange_rate_service(current_currency)