from httpx import AsyncClient, ASGITransport
import pytest

from main import app


@pytest.fixture
async def get_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client