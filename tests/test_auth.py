import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_registration():
    """
    Test the user registration endpoint.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/auth/register",
            json={"name": "VSEVOLOD melnyk", "username": "newuser", "password": "Test1234!"}
        )
        assert response.status_code == 400
        assert "detail" in response.json()

@pytest.mark.asyncio
async def test_login():
    """
    Test the user login endpoint.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/auth/login",
            json={"username": "newuser", "password": "Test1234!"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()