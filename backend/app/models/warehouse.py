# file: app/models/warehouse.py (SUDAH DIPERBAIKI)

from datetime import datetime
from sqlalchemy import (
    Integer, String, ForeignKey, Text, Enum as SQLAlchemyEnum, UniqueConstraint, DateTime, func
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
# ✅ LANGKAH 1: Impor hybrid_property
from sqlalchemy.ext.hybrid import hybrid_property
from typing import List, Optional

# Impor komponen dasar dan Enum yang relevan
from .base import BaseModel
from .enums import WarehouseStatusEnum, RackStatusEnum

# Impor tipe relasi untuk type hinting
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .type import TemperatureType, LocationType
    from .product import Allocation

class Warehouse(BaseModel):
    # ... (Tidak ada perubahan di sini) ...
    __tablename__ = 'warehouses'
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    address: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[WarehouseStatusEnum] = mapped_column(SQLAlchemyEnum(WarehouseStatusEnum, name="warehouse_status_enum", create_type=False), default=WarehouseStatusEnum.ACTIVE)
    temperature_type_id: Mapped[Optional[int]] = mapped_column(ForeignKey('temperature_types.id'))
    temperature_type: Mapped[Optional['TemperatureType']] = relationship(back_populates='warehouses')
    racks: Mapped[List['Rack']] = relationship(back_populates='warehouse')

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

class StockPlacement(BaseModel):
    # ... (Tidak ada perubahan di sini, model StockPlacement sudah benar) ...
    __tablename__ = 'stock_placements'
    rack_id: Mapped[int] = mapped_column(ForeignKey('racks.id'), nullable=False)
    allocation_id: Mapped[int] = mapped_column(ForeignKey('allocations.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    placed_by: Mapped[Optional[str]] = mapped_column(String(50))
    placement_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    rack: Mapped['Rack'] = relationship(back_populates='placement')
    allocation: Mapped['Allocation'] = relationship(back_populates='placements')
    __table_args__ = (UniqueConstraint('rack_id', name='uq_rack_id_placement'),)