from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Identity, Enum, DateTime, ForeignKey
from typing import TYPE_CHECKING
import enum
from datetime import datetime


if TYPE_CHECKING:
    from warehouse import Warehouse
    from transfertline import TransfertLine


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
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    source_warehouse: Mapped["Warehouse"] = relationship(
        "Warehouse",
        foreign_keys=[source_warehouse_id],
        back_populates="transfert_source"
    )
    destination_warehouse: Mapped["Warehouse"] = relationship(
        "Warehouse",
        foreign_keys=[destination_warehouse_id],
        back_populates="transfert_destination"
    )
    transfertline: Mapped["TransfertLine"] = relationship(
        "TransfertLine",
        back_populates="transfer"
    )

    def __repr__(self):
        return (
            f"source_warehouse_id = {self.source_warehouse_id},"
            f"destination_warehouse_id = {self.destination_warehouse_id},"
            f"status = {self.status},"
            f"created_at = {self.created_at}"
        )
