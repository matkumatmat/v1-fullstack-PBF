from datetime import datetime
from sqlalchemy import (
    Integer, String, ForeignKey, Text, Enum as SQLAlchemyEnum, UniqueConstraint, DateTime, func
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

    # ✅ LANGKAH 2: Tambahkan hybrid_property untuk current_quantity
    @hybrid_property
    def current_quantity(self) -> int:
        """
        Properti dinamis yang menghitung kuantitas saat ini di rak.
        Ini tidak disimpan di database, tetapi dihitung saat diakses.
        """
        if self.placement:
            return self.placement.quantity
        return 0

    def __repr__(self) -> str:
        return f"<Rack id={self.id} code='{self.code}'>"
