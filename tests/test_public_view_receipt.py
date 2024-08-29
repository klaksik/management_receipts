import pytest
from httpx import AsyncClient
from src.main import app


@pytest.mark.asyncio
async def test_public_view_receipt():
    """
    Test the public view receipt endpoint.

    This test ensures that the endpoint returns the expected response when
    viewing a receipt with a valid ID.

    Note: Make sure the receipt ID used in this test exists. You may need to
    set up a receipt creation method before this test runs.

    :raises AssertionError: If the response does not match the expected status and content
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        receipt_id = 1  # Ensure this ID exists or create one via a setup method

        response = await ac.get(f"/receipts/customer_receipts/{receipt_id}")

        assert response.status_code == 200
        assert "receipt_text" in response.json()