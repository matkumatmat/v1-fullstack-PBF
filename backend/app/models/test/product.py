# file: app/models/product.py

from datetime import date
from sqlalchemy import (
    Integer, String, ForeignKey, Date, Numeric, Text,
    Enum as SQLAlchemyEnum
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

# Impor komponen dasar dan Enum yang relevan
from .base import BaseModel
from .enums import AllocationStatusEnum

# Impor tipe relasi untuk type hinting
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .type import ProductType, PackageType, TemperatureType, ProductPrice, AllocationType
    from .order_process import SalesOrderItem
    from .customer import Customer
    from .warehouse import StockPlacement
    # Placeholder untuk model yang belum ada
    # class PickingOrderItem: pass
    # class PickingListItem: pass
    # class Consignment: pass
    # class StockMovement: pass
    # class TenderContract: pass


class Product(BaseModel):
    __tablename__ = 'products'
    
    # id, public_id, created_at, updated_at diwarisi dari BaseModel.
    # public_id = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False, index=True) # <-- DIGANTIKAN OLEH MIXIN

    product_code: Mapped[str] = mapped_column(String(25), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    manufacturer: Mapped[Optional[str]] = mapped_column(String(100))
    product_type_id: Mapped[int] = mapped_column(ForeignKey('product_types.id'), nullable=False)
    package_type_id: Mapped[int] = mapped_column(ForeignKey('package_types.id'), nullable=False)
    temperature_type_id: Mapped[int] = mapped_column(ForeignKey('temperature_types.id'), nullable=False)

    # --- Relationships ---
    batches: Mapped[List['Batch']] = relationship(back_populates='product')
    product_type: Mapped['ProductType'] = relationship(back_populates='products')
    package_type: Mapped['PackageType'] = relationship(back_populates='products')     
    temperature_type: Mapped['TemperatureType'] = relationship(back_populates='products')
    sales_order_items: Mapped[List['SalesOrderItem']] = relationship(back_populates='product')
    prices: Mapped[List['ProductPrice']] = relationship(back_populates='product', cascade='all, delete-orphan')

    # Merefaktor relasi yang dikomentari ke sintaks modern.
    # picking_order_items: Mapped[List['PickingOrderItem']] = relationship(back_populates='product')

    def __repr__(self) -> str:
        return f'<Product id={self.id} code="{self.product_code}" name="{self.name}">'

class Batch(BaseModel):
    __tablename__ = 'batches'
    lot_number: Mapped[str] = mapped_column(String(50), nullable=False)
    expiry_date: Mapped[date] = mapped_column(Date, nullable=False)
    NIE: Mapped[str] = mapped_column(String(50), nullable=False)
    received_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    receipt_document: Mapped[str] = mapped_column(String(25), nullable=False)
    receipt_date: Mapped[date] = mapped_column(Date, nullable=False)
    receipt_pic: Mapped[Optional[str]] = mapped_column(String(25))
    receipt_doc_url: Mapped[Optional[str]] = mapped_column(String(255))
    length: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    width: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    height: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    weight: Mapped[Optional[float]] = mapped_column(Numeric(10, 3))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)

    # --- Relationships ---
    product: Mapped['Product'] = relationship(back_populates='batches')
    allocations: Mapped[List['Allocation']] = relationship(back_populates='batch')
    
    # Merefaktor relasi yang dikomentari ke sintaks modern.
    # stock_movements: Mapped[List['StockMovement']] = relationship(back_populates='batch')

    ### DEVIL'S ADVOCATE NOTE ###
    # Menghapus semua properti agregat (`volume`, `total_shipped`, `last_stock`, dll.).
    # Properti ini adalah jebakan performa N+1 yang sangat serius. Mereka menyembunyikan
    # query yang mahal. Kalkulasi ini HARUS dilakukan secara eksplisit di service layer
    # menggunakan query SQL agregat (`func.sum()`) untuk performa yang dapat diprediksi.

    def __repr__(self) -> str:
        return f'<Batch id={self.id} lot_number="{self.lot_number}" product_id={self.product_id}>'

class Allocation(BaseModel):
    __tablename__ = 'allocations'
    
    # id, public_id, created_at, updated_at diwarisi dari BaseModel.
    # public_id = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False, index=True) # <-- DIGANTIKAN OLEH MIXIN

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
    # consignments: Mapped[List['Consignment']] = relationship(back_populates='allocation')
    # stock_movements: Mapped[List['StockMovement']] = relationship(back_populates='allocation')
    # tender_contract_id: Mapped[Optional[int]] = mapped_column(ForeignKey('tender_contracts.id'))
    # tender_contract: Mapped[Optional['TenderContract']] = relationship(back_populates='allocations')
    
    ### DEVIL'S ADVOCATE NOTE ###
    # Menghapus semua properti. Kalkulasi stok (`last_stock`, `available_stock`)
    # sangat rentan terhadap race condition dan masalah performa.
    # Logika ini HARUS berada di service layer, idealnya dalam transaksi database
    # atau menggunakan query agregat yang terkunci untuk memastikan konsistensi data.
    # Menaruhnya di model memberikan ilusi kesederhanaan yang berbahaya.

    def __repr__(self) -> str:
        return f'<Allocation id={self.id} number="{self.allocation_number}" batch_id={self.batch_id}>'