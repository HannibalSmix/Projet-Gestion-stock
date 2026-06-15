from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from models.transfert import Transfert, Status


def create_transfert(
    session: Session,
    source_warehouse_id: int,
    destination_warehouse_id: int,
    status: Status = Status.DRAFT,
    created_at: datetime = None
    ) :
    
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
    return session.get(Transfert, transfert_id)


def get_all_transferts(session: Session):
    return session.query(Transfert).all()


def get_transferts_by_status(session: Session, status: Status):
    return session.query(Transfert).filter(Transfert.status == status).all()


def get_transferts_by_source_warehouse(session: Session, warehouse_id: int):
    return session.query(Transfert).filter(Transfert.source_warehouse_id == warehouse_id).all()


def get_transferts_by_destination_warehouse(session: Session, warehouse_id: int):
    return session.query(Transfert).filter(Transfert.destination_warehouse_id == warehouse_id).all()


