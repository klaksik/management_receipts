import pytest
from httpx import AsyncClient
from src.main import app


@pytest.mark.asyncio
async def test_create_receipt(token_future):
    """
    Test the create receipt endpoint.

    :param token_future: Future for obtaining the authentication token
    """
    # Obtain the token from the future
    token = await token_future

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Set the header with the obtained token
        headers = {"Authorization": token}

        # Payload for creating a receipt
        payload = {
            "products": [
                {
                    "name": "Product1",
                    "price": 100.0,
                    "quantity": 2
                }
            ],
            "payment": {
                "type": "cash",
                "amount": 500.0
            }
        }

        # Send POST request to create a receipt
        response = await ac.post("/receipts/create_receipt", json=payload, headers=headers)

        # Assert the response
        assert response.status_code == 200
        assert "id" in response.json()