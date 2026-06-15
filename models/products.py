
from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Identity
from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from profil import Profiles
#     from post import Posts


class Products(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    active: Mapped[bool] = mapped_column(default=True)

    def __repr__(self):
        return f"name = {self.name}, sku= {self.sku}, active = {self.active}"