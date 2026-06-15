from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Identity, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from receipt import Receipt
    from products import Products


class ReceiptLine(Base):
    __tablename__ = "receiptline"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    receipt_id: Mapped[int] = mapped_column(ForeignKey("receipt.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    receipt: Mapped["Receipt"] = relationship(
        "Receipt",
        back_populates="receiptline",
        uselist=False
    )
    product: Mapped["Products"] = relationship(
        "Products",
        back_populates="receiptline",
        uselist=False
    )

    def __repr__(self):
        return (
            f"receipt_id = {self.receipt_id},"
            f"product_id = {self.product_id},"
            f"quantity = {self.quantity}"
        )

