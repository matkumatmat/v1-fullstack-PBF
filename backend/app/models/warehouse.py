# file: app/models/warehouse.py
from datetime import datetime
from sqlalchemy import (
    Integer, String, ForeignKey, Text, Enum as SQLAlchemyEnum, UniqueConstraint, DateTime, func
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
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
    # ... (Tidak ada perubahan di sini, model Warehouse sudah benar) ...
    __tablename__ = 'warehouses'
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    address: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[WarehouseStatusEnum] = mapped_column(SQLAlchemyEnum(WarehouseStatusEnum, name="warehouse_status_enum", create_type=False), default=WarehouseStatusEnum.ACTIVE)
    temperature_type_id: Mapped[Optional[int]] = mapped_column(ForeignKey('temperature_types.id'))
    temperature_type: Mapped[Optional['TemperatureType']] = relationship(back_populates='warehouses')
    racks: Mapped[List['Rack']] = relationship(back_populates='warehouse')

    def __repr__(self) -> str:
        return f'<Warehouse id={self.id} code="{self.code}" name="{self.name}">'

class Rack(BaseModel):
    __tablename__ = 'racks'

    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    
    ### DEVIL'S ADVOCATE NOTE ###
    # Menghapus `quantity` dan `allocation_id` dari Rack.
    # Rak adalah entitas fisik. Di mana barang diletakkan dan berapa jumlahnya
    # adalah informasi transaksional yang lebih baik disimpan di model terpisah (`StockPlacement`).
    # Ini mencegah redundansi data dan membuat model Rack lebih bersih dan stabil.
    
    capacity: Mapped[Optional[int]] = mapped_column(Integer) # Kapasitas fisik (opsional)
    status: Mapped[RackStatusEnum] = mapped_column(SQLAlchemyEnum(RackStatusEnum, name="rack_status_enum", create_type=False), default=RackStatusEnum.ACTIVE)
    
    zone: Mapped[Optional[str]] = mapped_column(String(10))
    row: Mapped[Optional[str]] = mapped_column(String(10))
    level: Mapped[Optional[str]] = mapped_column(String(10))
    
    warehouse_id: Mapped[int] = mapped_column(ForeignKey('warehouses.id'), nullable=False)
    location_type_id: Mapped[Optional[int]] = mapped_column(ForeignKey('location_types.id'))

    # --- Relationships ---
    warehouse: Mapped['Warehouse'] = relationship(back_populates='racks')
    location_type: Mapped[Optional['LocationType']] = relationship()
    
    ### DEVIL'S ADVOCATE NOTE ###
    # Relasi ke StockPlacement. Ini adalah hubungan One-to-One.
    # `uselist=False` memberitahu SQLAlchemy bahwa `rack.placement` akan menjadi satu objek, bukan list.
    # `cascade` memastikan jika Rak dihapus, penempatannya juga dihapus.
    placement: Mapped[Optional['StockPlacement']] = relationship(back_populates='rack', cascade="all, delete-orphan", uselist=False)
    
    def __repr__(self) -> str:
        return f"<Rack id={self.id} code='{self.code}'>"

class StockPlacement(BaseModel):
    """
    Model ini merepresentasikan peristiwa penempatan sejumlah kuantitas
    dari sebuah alokasi ke sebuah rak spesifik.
    Ini adalah "Association Object" yang diperkaya dengan data tambahan (quantity, placed_by, dll).
    """
    __tablename__ = 'stock_placements'
    
    rack_id: Mapped[int] = mapped_column(ForeignKey('racks.id'), nullable=False)
    allocation_id: Mapped[int] = mapped_column(ForeignKey('allocations.id'), nullable=False)
    
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    
    placed_by: Mapped[Optional[str]] = mapped_column(String(50))
    placement_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # --- Relationships ---
    rack: Mapped['Rack'] = relationship(back_populates='placement')
    allocation: Mapped['Allocation'] = relationship(back_populates='placements')

    __table_args__ = (
        ### DEVIL'S ADVOCATE NOTE ###
        # Ini adalah bagian paling KRITIS dari desain ini.
        # `UniqueConstraint('rack_id')` MENEGAKKAN aturan bisnis Anda di level database.
        # Ini memastikan bahwa sebuah `rack_id` hanya bisa muncul SATU KALI di tabel ini,
        # yang berarti satu rak hanya bisa memiliki satu penempatan.
        UniqueConstraint('rack_id', name='uq_rack_id_placement'),
    )

    def __repr__(self) -> str:
        return f"<StockPlacement rack_id={self.rack_id} alloc_id={self.allocation_id} qty={self.quantity}>"