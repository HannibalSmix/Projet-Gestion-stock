from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

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
    return session.get(Warehouse, warehouse_id)


def get_warehouse_by_name(session: Session, name: str):
    return session.query(Warehouse).filter(Warehouse.name == name).first()


def get_warehouse_by_location(session: Session, location: str):
    return session.query(Warehouse).filter(Warehouse.location == location).first()


def get_all_warehouses(session: Session):
    return session.query(Warehouse).all()

