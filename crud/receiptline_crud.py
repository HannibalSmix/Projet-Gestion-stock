from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from models.receiptline import ReceiptLine


def create_receipt_line(session: Session, receipt_id: int, product_id: int, quantity: int):
    receipt_line = ReceiptLine(
        receipt_id=receipt_id,
        product_id=product_id,
        quantity=quantity
    )
    try:
        session.add(receipt_line)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print(f"Erreur : {e.orig}")
    session.refresh(receipt_line)
    return receipt_line

def get_receipt_line(session: Session, receipt_line_id: int):
    stmt = select(ReceiptLine).where(ReceiptLine.id == receipt_line_id)
    return session.execute(stmt).scalar_one_or_none()


def get_lines_by_receipt(session: Session, receipt_id: int) -> list[ReceiptLine]:
    stmt = select(ReceiptLine).where(ReceiptLine.receipt_id == receipt_id)
    return session.execute(stmt).scalars().all()


def get_lines_by_product(session: Session, product_id: int) -> list[ReceiptLine]:
    stmt = select(ReceiptLine).where(ReceiptLine.product_id == product_id)
    return session.execute(stmt).scalars().all()
