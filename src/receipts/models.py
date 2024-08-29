from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, func
from sqlalchemy.orm import relationship
from src.database import Base


class SalesReceipt(Base):
    """
    Model to represent a sales receipt.

    :param id: Unique identifier of the sales receipt
    :param created_at: Timestamp when the sales receipt was created
    :param user_id: Identifier of the user who created the receipt
    :param user: Relationship to the User model
    :param items: Relationship to the SalesItem model
    :param total_amount: Total amount of the sales receipt
    :param payment_type: Type of payment for the sales receipt (e.g., cash, cashless)
    """
    __tablename__ = 'sales_receipts'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Identifier of the user who created the receipt
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='sales_receipts')

    # Relationship to items in the receipt
    items = relationship('SalesItem', back_populates='sales_receipt', cascade='all, delete-orphan')

    total_amount = Column(DECIMAL, nullable=False)
    payment_type = Column(String, nullable=False)


class SalesItem(Base):
    """
    Model to represent an item in a sales receipt.

    :param id: Unique identifier of the sales item
    :param sales_receipt_id: Identifier of the associated sales receipt
    :param sales_receipt: Relationship to the SalesReceipt model
    :param product_name: Name of the product
    :param quantity: Quantity of the product sold
    :param price: Price per unit of the product
    """
    __tablename__ = 'sales_items'

    id = Column(Integer, primary_key=True)

    # Identifier of the associated receipt
    sales_receipt_id = Column(Integer, ForeignKey('sales_receipts.id'), nullable=False)
    sales_receipt = relationship('SalesReceipt', back_populates='items')

    # Product information
    product_name = Column(String, nullable=False)
    quantity = Column(DECIMAL, nullable=False)
    price = Column(DECIMAL, nullable=False)