
from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Identity, ForeignKey
from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from profil import Profiles
#     from post import Posts


class Stocklevel(Base):
    __tablename__ = "stocklevel"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouse.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self):
        return f"product_id = {self.product_id}, warehouse_id = {self.warehouse_id}, quantity = {self.quantity}"