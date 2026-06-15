from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

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
    return session.get(Supplier, supplier_id)


def get_supplier_by_name(session: Session, name: str):
    return session.query(Supplier).filter(Supplier.name == name).first()


def get_supplier_by_email(session: Session, email: str):
    return session.query(Supplier).filter(Supplier.email == email).first()


def get_all_suppliers(session: Session):
    return session.query(Supplier).all()
