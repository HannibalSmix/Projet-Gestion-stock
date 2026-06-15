from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Identity, Enum, ForeignKey, Datetime
from typing import TYPE_CHECKING
import enum
from datetime import datetime

if TYPE_CHECKING:
    from receiptline import ReceiptLine
    from supplier import Supplier
    from warehouse import Warehouse


class Status(enum.Enum):
    DRAFT = 1
    DONE = 2
    CANCELLED = 3
    

class Receipt(Base):
    __tablename__ = "receipt"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("supplier.id"), nullable=False)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouse.id"), nullable=False)
    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False)
    created_at: Mapped[datetime] = mapped_column(Datetime, nullable=False)

    receiptline: Mapped["ReceiptLine"] = relationship(
        "ReceiptLine",
        back_populates="receipt"
    )

    supplier: Mapped["Supplier"] = relationship(
        "Supplier",
        back_populates="receipt",
        uselist=False
    )

    warehouse: Mapped["Warehouse"] = relationship(
        "Warehouse",
        back_populates="receipt",
        uselist=False
    )

    def __repr__(self):
        return (
            f"supplier_id = {self.supplier_id},"
            f"warehouse_id = {self.warehouse_id},"
            f"status = {self.status},"
            f"created_at = {self.created_at}"
        )

