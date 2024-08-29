from pydantic import BaseModel
from datetime import datetime
from typing import List
from decimal import Decimal


class User(BaseModel):
    """
    Schema representing a user.

    :param id: Unique identifier of the user
    :param username: Username of the user
    :param name: Full name of the user
    """
    id: int
    username: str
    name: str


class SalesItem(BaseModel):
    """
    Schema representing a sales item.

    :param product_name: Name of the product
    :param quantity: Quantity of the product sold
    :param price: Price per unit of the product
    """
    product_name: str
    quantity: Decimal
    price: Decimal


class SalesReceipt(BaseModel):
    """
    Schema representing a sales receipt.

    :param id: Unique identifier of the sales receipt
    :param created_at: Timestamp when the sales receipt was created
    :param user_id: ID of the user associated with the sales receipt
    :param total_amount: Total amount of the sales receipt
    :param payment_type: Type of payment for the sales receipt
    :param items: List of sales items included in the sales receipt
    """
    id: int
    created_at: datetime
    user_id: int
    total_amount: Decimal
    payment_type: str
    items: List[SalesItem] = []


class SalesReceiptView(BaseModel):
    """
    Schema representing a view of a sales receipt.

    :param receipt_text: Text representation of the sales receipt
    """
    receipt_text: str