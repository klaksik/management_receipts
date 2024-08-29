from datetime import datetime
from typing import List
from decimal import Decimal
from pydantic import BaseModel


class SalesItemResponse(BaseModel):
    """
    Response schema for a sales item.

    :param id: Unique identifier of the sales item
    :param product_name: Name of the product
    :param quantity: Quantity of the product sold
    :param price: Price per unit of the product
    """
    id: int
    product_name: str
    quantity: Decimal
    price: Decimal

    class Config:
        from_attributes = True  # Allow model to be created from ORM objects


class SalesReceiptResponse(BaseModel):
    """
    Response schema for a sales receipt.

    :param id: Unique identifier of the sales receipt
    :param created_at: Timestamp when the sales receipt was created
    :param total_amount: Total amount of the sales receipt
    :param payment_type: Type of payment for the sales receipt
    :param items: List of sales items included in the sales receipt
    """
    id: int
    created_at: datetime
    total_amount: Decimal
    payment_type: str
    items: List[SalesItemResponse]

    class Config:
        from_attributes = True  # Allow model to be created from ORM objects


class SalesReceiptListResponse(BaseModel):
    """
    Response schema for a list of sales receipts.

    :param receipts: List of sales receipt responses
    :param total_count: Total number of sales receipts
    """
    receipts: List[SalesReceiptResponse]
    total_count: int