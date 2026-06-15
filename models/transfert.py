from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Identity, Enum, Datetime, ForeignKey
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


class Transfert(Base):
    __tablename__ = "transfert"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    source_warehouse_id: Mapped[int] = mapped_column(
        ForeignKey("warehouse.id"), 
        nullable=False)
    destination_warehouse_id: Mapped[int] = mapped_column(
        ForeignKey("warehouse.id"), 
        nullable=False)
    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False)
    created_at: Mapped[datetime] = mapped_column(Datetime, nullable=False)

    def __repr__(self):
        return (
            f"source_warehouse_id = {self.source_warehouse_id},"
            f"destination_warehouse_id = {self.destination_warehouse_id},"
            f"status = {self.status},"
            f"created_at = {self.created_at}"
        )
