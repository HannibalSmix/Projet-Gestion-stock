from dotenv import load_dotenv
import os
from db.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from models.supplier import Supplier
from models.receipt import Receipt
from models.receiptline import ReceiptLine
from models.products import Products
from models.warehouse import Warehouse
from models.stocklevel import Stocklevel
from models.stockmove import Stockmove
from models.transfert import Transfert
from models.transfertline import TransfertLine

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DATABASE_URL, echo=True)


class Base(DeclarativeBase):
    pass