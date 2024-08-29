from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base

class User(Base):
    __tablename__ = "users"  # Define the table name as 'users'

    # Define the table columns
    id = Column(Integer, primary_key=True, index=True)  # Primary key, indexed for faster queries
    username = Column(String, unique=True)  # Unique username field
    name = Column(String, index=True)  # Name field, indexed
    hashed_password = Column(String)  # Hashed password field

    # Define the relationship to the SalesReceipt table
    sales_receipts = relationship('SalesReceipt', back_populates='user')