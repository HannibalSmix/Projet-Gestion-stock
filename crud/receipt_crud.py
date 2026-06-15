from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from models.receipt import Receipt, Status


def create_receipt(session: Session, supplier_id: int, warehouse_id: int, status: Status = Status.DRAFT):

    receipt = Receipt(
        supplier_id=supplier_id,
        warehouse_id=warehouse_id,
        status=status,
        created_at=datetime.now()
    )

    try:
        session.add(receipt)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print(f"Erreur : {e.orig}")

    session.refresh(receipt)
    return receipt

def get_receipt(session: Session, receipt_id: int):
    return session.get(Receipt, receipt_id)

def get_receipts_by_supplier(session: Session, supplier_id: int):
    return session.query(Receipt).filter(Receipt.supplier_id == supplier_id).all()

def get_receipts_by_warehouse(session: Session, warehouse_id: int) -> list[Receipt]:
    return session.query(Receipt).filter(Receipt.warehouse_id == warehouse_id).all()
