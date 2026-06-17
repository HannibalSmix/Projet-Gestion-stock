from db.database import engine
from sqlalchemy.orm import sessionmaker
from utils.export_csv import (
            export_suppliers_to_csv,
            export_products_to_csv,
            export_warehouse_to_csv,
            export_receipt_to_csv,
            export_receiptline_to_csv,
            export_stockmove_to_csv,
            export_transfert_to_csv,
            export_transfertline_to_csv,
            export_stocklevel_to_csv)

# Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

with SessionLocal() as session:
    # export_suppliers_to_csv(session)
    # export_products_to_csv(session)
    # export_warehouse_to_csv(session)
    # export_receipt_to_csv(session)
    # export_receiptline_to_csv(session)
    # export_stockmove_to_csv(session)
    # export_transfert_to_csv(session)
    # export_transfertline_to_csv(session)
    export_stocklevel_to_csv(session)
    print('Done')