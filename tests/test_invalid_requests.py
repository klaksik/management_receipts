import pytest
from httpx import AsyncClient
from src.main import app


@pytest.mark.asyncio
async def test_invalid_requests(token_future):
    """
    Test various invalid request scenarios for the receipts endpoints.

    :param token_future: Future for obtaining the authentication token
    """
    # Obtain the token from the future
    token = await token_future

    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = {"Authorization": token}

        # Test invalid product price
        response = await ac.post(
            "/receipts/create_receipt",
            json={
                "products": [{"name": "Product1", "price": "invalid_price", "quantity": 2}],
                "payment": {"type": "cash", "amount": 500}
            },
            headers=headers
        )
        assert response.status_code == 422

        # Test insufficient payment
        response = await ac.post(
            "/receipts/create_receipt",
            json={
                "products": [{"name": "Product1", "price": 100.0, "quantity": 2}],
                "payment": {"type": "cash", "amount": 100}
            },
            headers=headers
        )
        assert response.status_code == 400
        assert response.json().get(
            "detail") == "The amount you provided is not enough to cover the total cost of the items."

        # Test unauthorized access
        response = await ac.get("/receipts/view_receipts")
        assert response.status_code == 401

        # Test viewing non-existing receipt
        response = await ac.get("/receipts/view_receipts/9999", headers=headers)
        assert response.status_code == 404
        assert response.json().get("detail") == "Receipt not found"