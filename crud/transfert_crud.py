from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from sqlalchemy import select

from models.transfert import Transfert, Status


def create_transfert(
    session: Session,
    source_warehouse_id: int,
    destination_warehouse_id: int,
    status: Status = Status.DRAFT,
    created_at: datetime = None
):
    
    transfert = Transfert(
        source_warehouse_id=source_warehouse_id,
        destination_warehouse_id=destination_warehouse_id,
        status=status,
        created_at=created_at or datetime.now()
    )
    try:
        session.add(transfert)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print(f"Erreur : {e.orig}")
    session.refresh(transfert)
    return transfert


def get_transfert(session: Session, transfert_id: int):
    stmt = select(Transfert).where(Transfert.id == transfert_id)
    return session.execute(stmt).scalar_one_or_none()


def get_all_transferts(session: Session):
    stmt = select(Transfert)
    return session.execute(stmt).scalars().all()


def get_transferts_by_status(session: Session, status: Status):
    stmt = select(Transfert).where(Transfert.status == status)
    return session.execute(stmt).scalars().all()


def get_transferts_by_source_warehouse(session: Session, warehouse_id: int):
    stmt = select(Transfert).where(
        Transfert.source_warehouse_id == warehouse_id)
    return session.execute(stmt).scalars().all()


def get_transferts_by_destination_warehouse(session: Session, warehouse_id: int):
    stmt = select(Transfert).where(
        Transfert.destination_warehouse_id == warehouse_id)
    return session.execute(stmt).scalars().all()

