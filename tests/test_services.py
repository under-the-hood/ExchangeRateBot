import pytest

@pytest.mark.asyncio
async def test_get_current_exchange_rate(get_client):
    response = await get_client.get("/exchange_rates/get_exchange_rate")
    
    assert response.status_code == 200
    assert isinstance(response.json(), float)