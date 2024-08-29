from datetime import datetime
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.auth.models import User
from src.receipts.models import SalesReceipt
from src.receipts.view_receipts.schemas import SalesReceiptListResponse, SalesReceiptResponse, SalesItemResponse


async def get_receipts(
        user: User,
        db: AsyncSession,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        payment_type: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        offset: Optional[int] = None
) -> SalesReceiptListResponse:
    """
    Retrieve and filter sales receipts for a user.

    :param user: User object
    :param db: Asynchronous database session
    :param start_date: Start date for filtering receipts
    :param end_date: End date for filtering receipts
    :param min_amount: Minimum amount for filtering receipts
    :param max_amount: Maximum amount for filtering receipts
    :param payment_type: Payment type for filtering receipts
    :param page: Page number for pagination
    :param page_size: Number of items per page for pagination
    :param offset: Offset for pagination
    :return: A response schema containing the list of sales receipts and total count
    """
    # Build the query for retrieving receipts
    query = select(SalesReceipt).where(SalesReceipt.user_id == user.id).options(selectinload(SalesReceipt.items))

    if start_date:
        query = query.where(SalesReceipt.created_at >= start_date)
    if end_date:
        query = query.where(SalesReceipt.created_at <= end_date)
    if min_amount is not None:
        query = query.where(SalesReceipt.total_amount >= min_amount)
    if max_amount is not None:
        query = query.where(SalesReceipt.total_amount <= max_amount)
    if payment_type:
        query = query.where(SalesReceipt.payment_type == payment_type)

    # Handle pagination
    if page is not None and page_size is not None:
        offset_value = (page - 1) * page_size
    else:
        offset_value = offset if offset is not None else 0

    query = query.offset(offset_value)
    if page_size is not None:
        query = query.limit(page_size)

    async with db as session:
        # Execute the query to retrieve receipts
        result = await session.execute(query)
        receipts = result.scalars().all()

        # Construct a separate query to count total receipts
        count_query = select(SalesReceipt).where(SalesReceipt.user_id == user.id)
        if start_date:
            count_query = count_query.where(SalesReceipt.created_at >= start_date)
        if end_date:
            count_query = count_query.where(SalesReceipt.created_at <= end_date)
        if min_amount is not None:
            count_query = count_query.where(SalesReceipt.total_amount >= min_amount)
        if max_amount is not None:
            count_query = count_query.where(SalesReceipt.total_amount <= max_amount)
        if payment_type:
            count_query = count_query.where(SalesReceipt.payment_type == payment_type)

        count_result = await session.execute(count_query)
        total_count = len(count_result.fetchall())

    # Properly transform the receipts into response schemas
    receipt_responses = [
        SalesReceiptResponse(
            id=receipt.id,
            created_at=receipt.created_at,
            total_amount=receipt.total_amount,
            payment_type=receipt.payment_type,
            items=[SalesItemResponse.from_orm(item) for item in receipt.items]
        ) for receipt in receipts
    ]

    return SalesReceiptListResponse(
        receipts=receipt_responses,
        total_count=total_count
    )