
from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Identity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from transfert import Transfert
    from stockmove import Stockmove
    from stocklevel import Stocklevel
    from receipt import Receipt


class Warehouse(Base):
    __tablename__ = "warehouse"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    location: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    transfert_source: Mapped["Transfert"] = relationship(
        "Transfert",
        back_populates="warehouse"
    )
    transfert_destination: Mapped["Transfert"] = relationship(
        "Transfert",
        back_populates="warehouse"
    )

    stockmove_source: Mapped["Stockmove"] = relationship(
        "Stockmove",
        back_populates="warehouse"
    )
    stockmove_destination: Mapped["Stockmove"] = relationship(
        "Stockmove",
        back_populates="warehouse"
    )
    stocklevel: Mapped["Stocklevel"] = relationship(
        "Stocklevel",
        back_populates="warehouse"
    )
    receipt: Mapped["Receipt"] = relationship(
        "Receipt",
        back_populates="Warehouse"
    )

    def __repr__(self):
        return f"name = {self.name}, location= {self.location}"