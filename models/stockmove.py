
from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Identity, ForeignKey
from typing import TYPE_CHECKING
import enum
from sqlalchemy import Enum
from datetime import datetime

# if TYPE_CHECKING:
#     from profil import Profiles
#     from post import Posts


class Status(enum.Enum):
    DRAFT = 1
    DONE = 2
    CANCELLED = 3

class Type(enum.Enum):
    IN = 1
    OUT = 2
    TRANSFER = 3

class Stockmove(Base):
    __tablename__ = "stockmove"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    source_warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouse.id"), nullable=False)
    destination_warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouse.id"), nullable=False)
    type: Mapped[Type] = mapped_column(Enum(Type), nullable=False)
    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False)
    created_at: Mapped[datetime] = mapped_column()

    def __repr__(self):
        return (
            f"product_id = {self.product_id},"
            f"quantity = {self.quantity}, "
            f"source_warehouse_id = {self.source_warehouse_id},"
            f"destination_warehouse_id = {self.destination_warehouse_id}," 
            f"type = {self.type},"
            f"status = {self.status},"
            f"created_at = {self.created_at}"
            )