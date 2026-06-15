from db.database import Base, engine
from sqlalchemy.orm import sessionmaker

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

with SessionLocal() as session:
    print('hello')