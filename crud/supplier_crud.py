from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from models.supplier import Supplier


def create_supplier(session: Session, name: str, email: str):
    
    supplier = Supplier(name=name, email=email)
    try:
        session.add(supplier)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print(f"Erreur : {e.orig}")
    session.refresh(supplier)
    return supplier


def get_supplier(session: Session, supplier_id: int):
    stmt = select(Supplier).where(Supplier.id == supplier_id)
    return session.execute(stmt).scalar_one_or_none()


def get_supplier_by_name(session: Session, name: str):
    stmt = select(Supplier).where(Supplier.name == name)
    return session.execute(stmt).scalar_one_or_none()


def get_supplier_by_email(session: Session, email: str):
    stmt = select(Supplier).where(Supplier.email == email)
    return session.execute(stmt).scalar_one_or_none()


def get_all_suppliers(session: Session):
    stmt = select(Supplier)
    return session.execute(stmt).scalars().all()
