from sqlalchemy.orm import Session
from models.products import Products
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

def create_product(session: Session, name: str, sku: str, active: bool = True):

    product = Products(name=name, sku=sku, active=active)

    try:
        session.add(product)
        session.commit()
        session.refresh(product)
    except IntegrityError as e:
        session.rollback()
        print(f"Erreur : {e.orig}")

    return product


def get_product(session: Session, product_id: int):
    stmt = select(Products).where(Products.id == product_id)
    return session.execute(stmt).scalar_one_or_none()


def get_all_products(session: Session):
    stmt = select(Products)
    return session.execute(stmt).scalars().all()


def get_product_by_sku(session: Session, sku: str):
    stmt = select(Products).where(Products.sku == sku)
    return session.execute(stmt).scalar_one_or_none()


def deactivate_product(session: Session, product_id: int):
    
    product = get_product(Session, product_id)
    if not product:
        return None
    product.active = False

    try: 
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print(f"Erreur : {e.orig}")
        
    session.refresh(product)

    return product

def delete_product(session: Session, product_id: int):

    product = get_product(Session, product_id)
    if not product:
        return False
    
    try:
        session.delete(product)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print(f"Erreur : {e.orig}")
        return False
    
    return True