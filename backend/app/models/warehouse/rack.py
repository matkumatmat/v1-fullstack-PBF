from datetime import datetime
from sqlalchemy import (
    Integer, String, ForeignKey, Text, Enum as SQLAlchemyEnum, UniqueConstraint, DateTime, func, select, case
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from typing import List, Optional

from ..configuration import BaseModel, WarehouseStatusEnum, RackStatusEnum
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..configuration import TemperatureType, LocationType
    from ..product import Allocation
    from .warehouse import Warehouse
    from .stock_placement import StockPlacement

class Rack(BaseModel):
    __tablename__ = 'racks'

    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    capacity: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[RackStatusEnum] = mapped_column(SQLAlchemyEnum(RackStatusEnum, name="rack_status_enum", create_type=False), default=RackStatusEnum.ACTIVE)
    zone: Mapped[Optional[str]] = mapped_column(String(10))
    row: Mapped[Optional[str]] = mapped_column(String(10))
    level: Mapped[Optional[str]] = mapped_column(String(10))
    warehouse_id: Mapped[int] = mapped_column(ForeignKey('warehouses.id'), nullable=False)
    location_type_id: Mapped[Optional[int]] = mapped_column(ForeignKey('location_types.id'))

    # --- Relationships ---
    warehouse: Mapped['Warehouse'] = relationship(back_populates='racks')
    location_type: Mapped[Optional['LocationType']] = relationship()
    placement: Mapped[Optional['StockPlacement']] = relationship(back_populates='rack', cascade="all, delete-orphan", uselist=False)

    @hybrid_property
    def current_quantity(self) -> int:
        # Kode Python ini tetap ada untuk akses pada instance yang sudah di-load
        if self.placement:
            return self.placement.quantity
        return 0

    # ✅ ===================================================================
    # ✅ TAMBAHKAN EKSPRESI SQL INI
    # ✅ ===================================================================
    @current_quantity.expression
    def current_quantity(cls):
        """
        Menyediakan ekspresi SQL untuk menghitung current_quantity.
        Ini mencegah lazy loading dan error greenlet.
        """
        # Kita menggunakan subquery untuk mendapatkan kuantitas dari tabel stock_placements
        # yang terhubung ke Rack ini.
        # Jika tidak ada placement, coalesce akan mengubah NULL menjadi 0.
        return func.coalesce(
            select(StockPlacement.quantity)
            .where(StockPlacement.rack_id == cls.id)
            .scalar_subquery(),
            0
        )

    def __repr__(self) -> str:
        return f"<Rack id={self.id}'>"
