from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.exceptions import ReceiptNotFoundException
from src.receipts.models import SalesReceipt
from src.receipts.customer_receipts.schemas import SalesReceiptView


async def get_receipt_text(db: AsyncSession, receipt_id: int) -> SalesReceiptView:
    """
    Retrieve and format a sales receipt as text.

    :param db: Asynchronous database session
    :param receipt_id: ID of the sales receipt to retrieve
    :return: A view of the sales receipt with formatted text
    :raises ReceiptNotFoundException: If the receipt with the given ID is not found
    """
    async with db as session:
        # Query the sales receipt and include related items and user
        result = await session.execute(
            select(SalesReceipt)
            .where(SalesReceipt.id == receipt_id)
            .options(selectinload(SalesReceipt.items), selectinload(SalesReceipt.user))
        )
        receipt = result.scalars().first()

        if not receipt:
            raise ReceiptNotFoundException(receipt_id)

        # Format the receipt text
        receipt_lines = [
            f"ФОП {receipt.user.name if receipt.user else 'Невідомий користувач'}",
            "================================"
        ]

        for item in receipt.items:
            receipt_lines.append(f"{item.quantity:.2f} x {item.price:,.2f} {item.quantity * item.price:,.2f}")
            receipt_lines.append(item.product_name)

        receipt_lines.extend([
            "================================",
            f"СУМА {receipt.total_amount:,.2f}",
            f"{receipt.payment_type} {receipt.total_amount:,.2f}",
            f"Решта {0.00:,.2f}",
            "================================",
            f" {receipt.created_at.strftime('%d.%m.%Y %H:%M')} ",
            "Дякуємо за покупку!"
        ])

        return SalesReceiptView(receipt_text="\n".join(receipt_lines))