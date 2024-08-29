from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import List, Literal


class Payment(BaseModel):
    """
    Represents a payment in a sale receipt.

    :param type: Type of payment ('cash' or 'cashless')
    :param amount: Amount of money paid
    """
    type: Literal['cash', 'cashless']
    amount: Decimal


class ProductCreate(BaseModel):
    """
    Schema for creating a new product.

    :param name: Name of the product
    :param price: Price of the product
    :param quantity: Quantity of the product
    """
    name: str
    price: Decimal
    quantity: int


class SaleReceiptCreate(BaseModel):
    """
    Schema for creating a new sale receipt.

    :param products: List of products included in the sale
    :param payment: Payment details for the sale
    """
    products: List[ProductCreate]
    payment: Payment


class ProductResponse(BaseModel):
    """
    Response schema for a product in a sale receipt.

    :param name: Name of the product
    :param price: Price of the product
    :param quantity: Quantity of the product
    :param total: Total cost for the product (price * quantity)
    """
    name: str
    price: Decimal
    quantity: int
    total: Decimal


class SaleReceiptResponse(BaseModel):
    """
    Response schema for a sale receipt.

    :param id: Unique identifier for the sale receipt
    :param products: List of products included in the sale
    :param payment: Payment details for the sale
    :param rest: Remaining amount after payment
    :param total: Total cost for the sale receipt
    :param created_at: Timestamp of when the sale receipt was created
    """
    id: int
    products: List[ProductResponse]
    payment: Payment
    rest: Decimal
    total: Decimal
    created_at: datetime