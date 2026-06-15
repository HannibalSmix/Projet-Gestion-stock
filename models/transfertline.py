from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Identity, Enum, Datetime, ForeignKey
from typing import TYPE_CHECKING
import enum
from datetime import datetime

# if TYPE_CHECKING:
#     from profil import Profiles
#     from post import Posts


class Status(enum.Enum):
    DRAFT = 1
    DONE = 2
    CANCELLED = 3


class TransfertLine(Base):
    __tablename__ = "transfertline"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    transfer_id: Mapped[int] = mapped_column(
        ForeignKey("transfert.id"), 
        nullable=False)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), 
        nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
 
    def __repr__(self):
        return (
            f"transfer_id = {self.transfer_id},"
            f"destination_warehouse_id = {self.destination_warehouse_id},"
            f"product_id = {self.product_id},"
            f"quantity = {self.quantity}"
        )
