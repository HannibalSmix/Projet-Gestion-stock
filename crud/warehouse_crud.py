from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from models.warehouse import Warehouse


def create_warehouse(session: Session, name: str, location: str):
    warehouse = Warehouse(name=name, location=location)
    try:
        session.add(warehouse)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print(f"Erreur : {e.orig}")
    session.refresh(warehouse)
    return warehouse


def get_warehouse(session: Session, warehouse_id: int):
    stmt = select(Warehouse).where(Warehouse.id == warehouse_id)
    return session.execute(stmt).scalar_one_or_none()


def get_warehouse_by_name(session: Session, name: str):
    stmt = select(Warehouse).where(Warehouse.name == name)
    return session.execute(stmt).scalar_one_or_none()


def get_warehouse_by_location(session: Session, location: str):
    stmt = select(Warehouse).where(Warehouse.location == location)
    return session.execute(stmt).scalar_one_or_none()


def get_all_warehouses(session: Session):
    stmt = select(Warehouse)
    return session.execute(stmt).scalars().all()
