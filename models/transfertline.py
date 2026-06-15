from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Identity, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from transfert import Transfert
    from products import Products


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
