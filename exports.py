from db.database import engine
from sqlalchemy.orm import sessionmaker

from utils.export_csv import export_suppliers_to_csv

# Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

with SessionLocal() as session:
    export_suppliers_to_csv(session)
    print('Done')