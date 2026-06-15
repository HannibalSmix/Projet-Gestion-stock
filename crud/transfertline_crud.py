from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.transfertline import TransfertLine


def create_transfert_line(
    session: Session,
    transfer_id: int,
    product_id: int,
    quantity: int
    ) :

    transfert_line = TransfertLine(
        transfer_id=transfer_id,
        product_id=product_id,
        quantity=quantity
    )
    try:
        session.add(transfert_line)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print(f"Erreur : {e.orig}")
    session.refresh(transfert_line)
    return transfert_line


def get_transfert_line(session: Session, transfert_line_id: int):
    return session.get(TransfertLine, transfert_line_id)


def get_lines_by_transfert(session: Session, transfer_id: int):
    return session.query(TransfertLine).filter(TransfertLine.transfer_id == transfer_id).all()


def get_lines_by_product(session: Session, product_id: int):
    return session.query(TransfertLine).filter(TransfertLine.product_id == product_id).all()

