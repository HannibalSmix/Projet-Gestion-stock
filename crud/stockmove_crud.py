from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from models.stockmove import Stockmove, Status, Type


def create_stock_move(
    session: Session,
    product_id: int,
    quantity: int,
    source_warehouse_id: int,
    destination_warehouse_id: int,
    type: Type,
    status: Status = Status.DRAFT,
    created_at: datetime = None
    ):

    stock_move = Stockmove(
        product_id=product_id,
        quantity=quantity,
        source_warehouse_id=source_warehouse_id,
        destination_warehouse_id=destination_warehouse_id,
        type=type,
        status=status,
        created_at=datetime.now()
    )
    try:
        session.add(stock_move)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print(f"Erreur : {e.orig}")
    session.refresh(stock_move)
    return stock_move


def get_stock_move(session: Session, stock_move_id: int):
    return session.get(Stockmove, stock_move_id)


def get_all_stock_moves(session: Session):
    return session.query(Stockmove).all()


def get_stock_moves_by_product(session: Session, product_id: int):
    return session.query(Stockmove).filter(Stockmove.product_id == product_id).all()


def get_stock_moves_by_source_warehouse(session: Session, warehouse_id: int):
    return session.query(Stockmove).filter(Stockmove.source_warehouse_id == warehouse_id).all()


def get_stock_moves_by_destination_warehouse(session: Session, warehouse_id: int):
    return session.query(Stockmove).filter(Stockmove.destination_warehouse_id == warehouse_id).all()

