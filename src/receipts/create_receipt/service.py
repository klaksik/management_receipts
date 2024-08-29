from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.receipts.models import SalesReceipt, SalesItem
from src.receipts.create_receipt.schemas import SaleReceiptCreate, SaleReceiptResponse, ProductResponse


async def create_sale_receipt(db: AsyncSession, receipt_data: SaleReceiptCreate, user_id: int,
                              total: Decimal) -> SaleReceiptResponse:
    """
    Create a sale receipt and store it in the database.

    :param db: Asynchronous database session
    :param receipt_data: Schema containing the sale receipt details
    :param user_id: ID of the user creating the receipt
    :param total: Total amount of the sale
    :return: Response schema containing the sale receipt details
    :raises HTTPException: If there's an error with the database or other unexpected errors
    """
    try:
        # Calculate the remaining amount after payment
        rest = receipt_data.payment.amount - total

        # Create the sale receipt record
        sales_receipt = SalesReceipt(
            user_id=user_id,
            total_amount=total,
            payment_type=receipt_data.payment.type  # Extract payment type as string
        )
        db.add(sales_receipt)
        await db.flush()  # Ensure the receipt ID is generated

        # Add products to the sale receipt
        products_response = []
        for product in receipt_data.products:
            sales_item = SalesItem(
                sales_receipt_id=sales_receipt.id,
                product_name=product.name,
                quantity=product.quantity,
                price=product.price,
            )
            db.add(sales_item)
            products_response.append(
                ProductResponse(
                    name=product.name,
                    price=product.price,
                    quantity=product.quantity,
                    total=product.price * product.quantity
                )
            )

        await db.commit()  # Commit the transaction

        # Create the response
        response = SaleReceiptResponse(
            id=sales_receipt.id,
            products=products_response,
            payment=receipt_data.payment,
            total=total,
            rest=rest,
            created_at=sales_receipt.created_at
        )
        return response

    except SQLAlchemyError:
        # Rollback in case of a SQLAlchemy error
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        # Rollback for any other exceptions
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
