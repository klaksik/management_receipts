import asyncio
import pytest
from httpx import AsyncClient
from src.main import app


# A fixture to get an authentication token, scope is set to session to reuse across multiple tests
@pytest.fixture(scope="session")
async def get_token():
    """
    Fixture to obtain an access token for authentication.

    :return: Bearer token as a string
    :raises ValueError: If the access token is not found in the response
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/login", json={"username": "newuser", "password": "Test1234!"})
        response_json = response.json()
        token = response_json.get('access_token')  # Use .get() to avoid KeyError if not found

        if not token:
            raise ValueError("Access token not found in response")

    return f'Bearer {token}'


@pytest.fixture(scope="session")
def token_future(get_token):
    """
    Fixture to ensure the token is available for multiple uses.

    :param get_token: The async get_token fixture to obtain the token
    :return: Future that represents the token retrieval
    """
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_token)
    loop.run_until_complete(future)  # Partially complete the future to avoid RuntimeError
    return future