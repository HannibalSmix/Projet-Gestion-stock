from sqlalchemy.orm import Session
from models.products import Products
from sqlalchemy.exc import IntegrityError

def create_product(session: Session, name: str, sku: str, active: bool = True):

    product = Products(name=name, sku=sku, active=active)

    try:
        session.add(product)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print(f"Erreur : {e.orig}")

    session.refresh(product)

    return product

def get_product(session: Session, product_id: int):
    return session.get(Products, product_id)

def get_product_by_sku(session: Session, sku: str):
    return session.query(Products).filter(Products.sku == sku).first()

def deactivate_product(session: Session, product_id: int):
    
    product = session.get(Products, product_id)
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

    product = session.get(Products, product_id)
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