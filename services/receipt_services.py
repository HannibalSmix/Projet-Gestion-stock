from sqlalchemy.orm import Session
from crud.receipt_crud import get_receipt
from crud.receiptline_crud import get_lines_by_receipt
from models.receipt import Status


def validate_receipt(session: Session, receipt_id: int):

    receipt = get_receipt(Session, receipt_id)
    if not receipt:
        print(f'No receipt found with id = {receipt_id}')
        return False
    
    if receipt.status != Status.DRAFT:
        pass

    lines = get_lines_by_receipt(Session, receipt_id)
    if not lines:
        print(f'No lines found for receipt = {receipt_id}')
        return False
    
    for line in lines:
        #maj stock
        
        pass
        
        #save in stockmove

    #DRAFT -> DONE
