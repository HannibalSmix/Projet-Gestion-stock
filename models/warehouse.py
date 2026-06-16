
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
        foreign_keys="Transfert.source_warehouse_id",
        back_populates="source_warehouse"
    )
    transfert_destination: Mapped["Transfert"] = relationship(
        "Transfert",
        foreign_keys="Transfert.destination_warehouse_id",
        back_populates="destination_warehouse"
    )

    stockmove_source: Mapped["Stockmove"] = relationship(
        "Stockmove",
        foreign_keys="Stockmove.source_warehouse_id",
        back_populates="source_warehouse"
    )
    stockmove_destination: Mapped["Stockmove"] = relationship(
        "Stockmove",
        foreign_keys="Stockmove.destination_warehouse_id",
        back_populates="destination_warehouse"
    )
    stocklevel: Mapped["Stocklevel"] = relationship(
        "Stocklevel",
        back_populates="warehouse"
    )
    receipt: Mapped["Receipt"] = relationship(
        "Receipt",
        back_populates="warehouse"
    )

    def __repr__(self):
        return f"name = {self.name}, location= {self.location}"