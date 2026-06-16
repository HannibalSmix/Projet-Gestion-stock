from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

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
    stmt = select(Stocklevel).where(Stocklevel.id == stock_level_id)
    return session.execute(stmt).scalar_one_or_none()


def get_stock_by_product(session: Session, product_id: int):
    stmt = select(Stocklevel).where(Stocklevel.product_id == product_id)
    return session.execute(stmt).scalars().all()


def get_stock_by_warehouse(session: Session, warehouse_id: int):
    stmt = select(Stocklevel).where(Stocklevel.warehouse_id == warehouse_id)
    return session.execute(stmt).scalars().all()


def get_stock_by_product_and_warhouse(session: Session, product_id: int, warehouse_id: int):
    stmt = select(Stocklevel).where(Stocklevel.product_id == product_id and Stocklevel.warehouse_id == warehouse_id)
    return session.execute(stmt).scalar_one_or_none()


def update_stock_quantity(session: Session, stocklevel_id: int, quantity: int):
    stmt = select(Stocklevel).where(Stocklevel.id == stocklevel_id)
    stock_level = session.execute(stmt).scalar_one_or_none()
    if not stock_level:
        return None
    stock_level.quantity += quantity
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print(f"Erreur : {e.orig}")
    session.refresh(stock_level)
    return stock_level
