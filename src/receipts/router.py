from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.auth.models import User
from src.receipts.customer_receipts.schemas import SalesReceiptView
from src.receipts.customer_receipts.service import get_receipt_text
from src.receipts.dependencies import get_user_id, get_user
from src.database import get_db
from src.exceptions import InsufficientPaymentException
from src.receipts.create_receipt.schemas import SaleReceiptCreate, SaleReceiptResponse
from src.receipts.create_receipt.service import create_sale_receipt
from src.receipts.models import SalesReceipt
from src.receipts.view_receipts.schemas import SalesReceiptListResponse, SalesReceiptResponse
from src.receipts.view_receipts.service import get_receipts

receipts_router = APIRouter()


@receipts_router.post("/create_receipt", response_model=SaleReceiptResponse)
async def create_receipt(
        receipt_data: SaleReceiptCreate,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_user_id)
):
    """
    Create a new sales receipt.

    :param receipt_data: Data for creating the receipt
    :param db: Database session
    :param user_id: ID of the user creating the receipt
    :return: Response with the created receipt details
    :raises InsufficientPaymentException: If the payment amount is less than the total
    """
    # Calculate the total amount for the receipt
    total = Decimal(sum(item.price * item.quantity for item in receipt_data.products))

    # Check if the payment amount is sufficient
    if receipt_data.payment.amount < total:
        raise InsufficientPaymentException()

    return await create_sale_receipt(db=db, receipt_data=receipt_data, user_id=user_id, total=total)


@receipts_router.get("/view_receipts", response_model=SalesReceiptListResponse)
async def view_receipts(
        start_date: Optional[datetime] = Query(None),
        end_date: Optional[datetime] = Query(None),
        min_amount: Optional[float] = Query(None),
        max_amount: Optional[float] = Query(None),
        payment_type: Optional[str] = Query(None),
        page: Optional[int] = Query(None, ge=1),
        page_size: Optional[int] = Query(None, ge=1),
        offset: Optional[int] = Query(None, ge=0),
        user: User = Depends(get_user),
        db: AsyncSession = Depends(get_db)
):
    """
    View a list of sales receipts with optional filters.

    :param start_date: Filter receipts created after this date
    :param end_date: Filter receipts created before this date
    :param min_amount: Filter receipts with a minimum amount
    :param max_amount: Filter receipts with a maximum amount
    :param payment_type: Filter receipts by payment type
    :param page: Page number for pagination
    :param page_size: Number of items per page for pagination
    :param offset: Offset for pagination
    :param user: User object
    :param db: Database session
    :return: Response with the list of filtered receipts and total count
    """
    return await get_receipts(
        user=user,
        db=db,
        start_date=start_date,
        end_date=end_date,
        min_amount=min_amount,
        max_amount=max_amount,
        payment_type=payment_type,
        page=page,
        page_size=page_size,
        offset=offset
    )


@receipts_router.get("/view_receipts/{receipt_id}", response_model=SalesReceiptResponse)
async def get_receipt_by_id(
        receipt_id: int,
        user: User = Depends(get_user),
        db: AsyncSession = Depends(get_db)
):
    """
    Get a sales receipt by its ID.

    :param receipt_id: ID of the receipt to retrieve
    :param user: User object
    :param db: Database session
    :return: Response with the receipt details
    :raises HTTPException: If the receipt is not found or does not belong to the user
    """
    async with db as session:
        receipt = await session.get(SalesReceipt, receipt_id, options=[selectinload(SalesReceipt.items)])
        if not receipt or receipt.user_id != user.id:
            raise HTTPException(status_code=404, detail="Receipt not found")
        return SalesReceiptResponse.from_orm(receipt)


@receipts_router.get("/customer_receipts/{receipt_id}", response_model=SalesReceiptView)
async def customer_receipts(
        receipt_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    Get a formatted view of a customer's receipt.

    :param receipt_id: ID of the receipt to retrieve
    :param db: Database session
    :return: Response with the formatted receipt view
    """
    receipt = await get_receipt_text(db, receipt_id)
    return receipt