from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.stocklevel import Stocklevel


def create_stock_level(session: Session, product_id: int, warehouse_id: int, quantity: int):
    stock_level = Stocklevel(
        product_id=product_id,
        warehouse_id=warehouse_id,
        quantity=quantity
    )
    try:
        session.add(stock_level)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print(f"Erreur : {e.orig}")
    session.refresh(stock_level)
    return stock_level


def get_stock_level(session: Session, stock_level_id: int):
    return session.get(Stocklevel, stock_level_id)

def get_stock_by_product(session: Session, product_id: int):
    return session.query(Stocklevel).filter(Stocklevel.product_id == product_id).all()


def get_stock_by_warehouse(session: Session, warehouse_id: int):
    return session.query(Stocklevel).filter(Stocklevel.warehouse_id == warehouse_id).all()

