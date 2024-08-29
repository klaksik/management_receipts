import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_view_receipts(token_future):
    """
    Test the view receipts endpoint without any filters or pagination.

    :param token_future: Future for obtaining the authentication token
    """
    # Get the token from the future
    token = await token_future

    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = {"Authorization": token}

        response = await ac.get("/receipts/view_receipts", headers=headers)

        assert response.status_code == 200
        assert isinstance(response.json().get("receipts"), list)

@pytest.mark.asyncio
async def test_view_receipts_with_pagination(token_future):
    """
    Test the view receipts endpoint with pagination.

    :param token_future: Future for obtaining the authentication token
    """
    # Get the token from the future
    token = await token_future

    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = {"Authorization": token}

        response = await ac.get("/receipts/view_receipts?page=1&size=2", headers=headers)

        assert response.status_code == 200
        assert isinstance(response.json().get("receipts"), list)

@pytest.mark.asyncio
async def test_view_receipts_with_filtering(token_future):
    """
    Test the view receipts endpoint with a date filter.

    :param token_future: Future for obtaining the authentication token
    """
    # Get the token from the future
    token = await token_future

    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = {"Authorization": token}

        response = await ac.get("/receipts/view_receipts?date=2023-01-01", headers=headers)

        assert response.status_code == 200
        assert isinstance(response.json().get("receipts"), list)