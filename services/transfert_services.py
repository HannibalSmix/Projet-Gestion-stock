from sqlalchemy.orm import Session
from models.transfert import Status
from crud.transfert_crud import get_transfert, update_status
from crud.transfertline_crud import get_lines_by_transfert
from crud.stocklevel_crud import get_stock_by_product_and_warehouse, create_stock_level, update_quantity
from crud.stockmove_crud import create_stock_move
from models.stockmove import Status as MoveStatus, Type


def validate_transfert(session: Session, transfert_id: int):

    transfert = get_transfert(session, transfert_id)
    if not transfert:
        print(f"No transfert found with id = {transfert_id}.")
        return False

    if transfert.status != Status.DRAFT:
        print(f"Transfert {transfert_id} has status {transfert.status}, cannot be validated.")
        return False

    # Retrieve transfert lines
    transfert_lines = get_lines_by_transfert(session, transfert_id)
    if not transfert_lines:
        print(f"No transfert lines found for transfert = {transfert_id}.")
        return False

    # Check if stock is enough for all transfertline before modifications
    for transfert_line in transfert_lines:
        stock_level = get_stock_by_product_and_warehouse(
            session, 
            transfert_line.product_id, 
            transfert.source_warehouse_id)
        
        available_quantity = 0 
        if stock_level:
            available_quantity = stock_level.quantity
        
        if available_quantity < transfert_line.quantity:
            print(f"Not enough stock for the product {transfert_line.product_id} "
                  f"in warehouse {transfert.source_warehouse_id}. "
                  f"Available : {available_quantity}, asked : {transfert_line.quantity}.")
            return False

    for transfert_line in transfert_lines:

        # Take from source warehouse
        update_quantity(session, 
                        transfert_line.id,
                        -transfert_line.quantity)

        # put in source warehouse
        # check if stock_level exist else create
        stock_level_dest = get_stock_by_product_and_warehouse(session, 
                                                            transfert_line.product_id, 
                                                            transfert.destination_warehouse_id)
        
        if stock_level_dest:
            update_quantity(session, 
                            transfert_line.id,
                            transfert_line.quantity)
        else:
            create_stock_level( session, 
                                transfert_line.product_id,
                                transfert.destination_warehouse_id,
                                transfert_line.quantity)

        # Create stockmove
        create_stock_move(
            session,
            transfert_line.product_id,
            transfert_line.quantity,
            transfert.source_warehouse_id,
            transfert.destination_warehouse_id,
            Type.TRANSFER,
            MoveStatus.DONE
        )

    update_status(session, transfert_id, Status.DONE)
    print(f"Transfert {transfert_id} validated !")
    return True


def cancel_transfert(session: Session, transfert_id: int):

    transfert = get_transfert(session, transfert_id)
    if not transfert:
        print(f"Transfert {transfert_id} not found.")
        return False

    if transfert.status != Status.DRAFT:
        print(f"Transfert {transfert_id} status is {transfert.status.name}, cannot be cancelled.")
        return False

    update_status(session, transfert_id, Status.CANCELLED)
    print(f"Transfert {transfert_id} is cancelled.")
    return True