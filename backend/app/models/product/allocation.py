from datetime import date
from sqlalchemy import (
    Integer, String, ForeignKey, Date, Numeric, Text,
    Enum as SQLAlchemyEnum
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

from ..configuration import BaseModel,AllocationStatusEnum
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..configuration import ProductType, PackageType, TemperatureType, ProductPrice, AllocationType
    from ..order_process import SalesOrderItem
    from ..users import Customer
    from ..warehouse import StockPlacement
    from .batch import Batch
    from ..process import Consignment
    from ..process import TenderContract

class Allocation(BaseModel):
    __tablename__ = 'allocations'
    allocated_quantity: Mapped[int] = mapped_column(Integer, default=0) 
    shipped_quantity: Mapped[int] = mapped_column(Integer, default=0)   
    reserved_quantity: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[AllocationStatusEnum] = mapped_column(SQLAlchemyEnum(AllocationStatusEnum, name="allocation_status_enum", create_type=False), default=AllocationStatusEnum.ACTIVE)
    allocation_number: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True, index=True)
    allocation_date: Mapped[date] = mapped_column(Date, nullable=False) # Default dihilangkan, lebih baik diatur di service.
    expiry_date: Mapped[Optional[date]] = mapped_column(Date)
    priority_level: Mapped[int] = mapped_column(Integer, default=5)
    special_instructions: Mapped[Optional[str]] = mapped_column(Text)
    handling_requirements: Mapped[Optional[str]] = mapped_column(Text)
    unit_cost: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    total_value: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))

    batch_id: Mapped[int] = mapped_column(ForeignKey('batches.id'), nullable=False)
    allocation_type_id: Mapped[int] = mapped_column(ForeignKey('allocation_types.id'), nullable=False)
    customer_id: Mapped[Optional[int]] = mapped_column(ForeignKey('customers.id'))
    
    original_reserved_quantity: Mapped[int] = mapped_column(Integer, default=0)
    customer_allocated_quantity: Mapped[int] = mapped_column(Integer, default=0)

    # --- Relationships ---
    batch: Mapped['Batch'] = relationship(back_populates='allocations')
    allocation_type: Mapped['AllocationType'] = relationship(back_populates='allocations')
    customer: Mapped[Optional['Customer']] = relationship(back_populates='allocations')  
    
    ### DEVIL'S ADVOCATE NOTE ###
    # REFAKTOR KRITIS: Mengganti relasi `racks` dan `rack_allocations` dengan `placements`.
    # Ini adalah sisi "One-to-Many" dari relasi dengan `StockPlacement`.
    # Satu Alokasi bisa memiliki BANYAK penempatan di rak yang berbeda.
    placements: Mapped[List['StockPlacement']] = relationship(back_populates='allocation')
    
    # Menghapus relasi lama yang kontradiktif.
    # racks = relationship('Rack', back_populates='allocation') # <-- DIGANTI
    # rack_allocations = relationship("RackAllocation", back_populates="allocation", cascade="all, delete-orphan") # <-- DIHAPUS

    # Merefaktor relasi yang dikomentari ke sintaks modern.
    # picking_order_items: Mapped[List['PickingOrderItem']] = relationship(back_populates='allocation')
    # picking_list_items: Mapped[List['PickingListItem']] = relationship(back_populates='allocation')
    consignments: Mapped[List['Consignment']] = relationship(back_populates='allocation')
    # stock_movements: Mapped[List['StockMovement']] = relationship(back_populates='allocation')
    #tender_contract_id: Mapped[Optional[int]] = mapped_column(ForeignKey('tender_contracts.id'))
    #tender_contract: Mapped[Optional['TenderContract']] = relationship(back_populates='allocations')
    
    ### DEVIL'S ADVOCATE NOTE ###
    # Menghapus semua properti. Kalkulasi stok (`last_stock`, `available_stock`)
    # sangat rentan terhadap race condition dan masalah performa.
    # Logika ini HARUS berada di service layer, idealnya dalam transaksi database
    # atau menggunakan query agregat yang terkunci untuk memastikan konsistensi data.
    # Menaruhnya di model memberikan ilusi kesederhanaan yang berbahaya.

    def __repr__(self) -> str:
        return f'<Allocation id={self.id} number="{self.allocation_number}" batch_id={self.batch_id}>'    