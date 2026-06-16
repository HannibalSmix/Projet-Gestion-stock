from sqlalchemy.orm import Session
from crud.receipt_crud import get_receipt, update_status
from crud.receiptline_crud import get_lines_by_receipt
from crud.stocklevel_crud import get_stock_by_product_and_warhouse, create_stock_level, update_stock_quantity
from crud.stockmove_crud import create_stock_move
from models.receipt import Status
from models.stockmove import Type


def validate_receipt(session: Session, receipt_id: int):

    receipt = get_receipt(Session, receipt_id)
    if not receipt:
        print(f'No receipt found with id = {receipt_id}')
        return False
    
    if receipt.status != Status.DRAFT:
        print(f"Receipt {receipt.id} has status: {receipt.status}, cannot be validated")
        return False

    receipt_lines = get_lines_by_receipt(Session, receipt_id)
    if not receipt_lines:
        print(f'No receipt lines found for receipt = {receipt_id}')
        return False
    
    for receipt_line in receipt_lines:
        # maj stocklevel
        stock_level = get_stock_by_product_and_warhouse(
            Session, receipt_line.product_id, receipt.warehouse_id)
        if not stock_level:
            stock_level = create_stock_level(
                Session, receipt_line.product_id,
                receipt.warehouse_id,
                receipt_line.quantity)
        else:
            stock_level = update_stock_quantity(
                Session, stock_level.id,
                receipt_line.quantity)
        
        # save in stockmove
        create_stock_move(
            Session,
            receipt_line.product_id,
            receipt_line.quantity,
            receipt.warehouse_id,
            receipt.warehouse_id,
            Type.IN,
            Status.DONE
        )

    #DRAFT -> DONE
    update_status(session, receipt_id, Status.DONE)
    print(f"Receipt {receipt.id} has been validated")
    return True


def cancel_receipt(session: Session, receipt_id: int):
    
    receipt = get_receipt(Session, receipt_id)
    if not receipt:
        print(f'No receipt found with id = {receipt_id}')
        return False
    
    if receipt.status != Status.DRAFT:
        print(f"Receipt {receipt.id} has a status: {receipt.status} and cannot be cancelled")
        return False    

    update_status(session, receipt_id, Status.CANCELLED)
    print(f"Receipt {receipt.id} has been cancelled")
    return True