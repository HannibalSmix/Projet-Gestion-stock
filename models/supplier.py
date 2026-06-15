
from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Identity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from receipt import Receipt


class Supplier(Base):
    __tablename__ = "supplier"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    receipt: Mapped["Receipt"] = relationship(
        "Receipt",
        back_populates="supplier"
    )

    
    def __repr__(self):
        return f"name = {self.name}, email= {self.email}"