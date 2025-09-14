from datetime import date
from sqlalchemy import (
    Integer, String, ForeignKey, Date, Numeric, Text,
    Enum as SQLAlchemyEnum
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

# Impor komponen dasar dan Enum yang relevan
from ..configuration import BaseModel,AllocationStatusEnum

# Impor tipe relasi untuk type hinting
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..configuration import ProductType, PackageType, TemperatureType, ProductPrice, AllocationType
    from ..order_process import SalesOrderItem
    from ..users import Customer
    from ..warehouse import StockPlacement
    from .product import Product
    from .allocation import Allocation, allocation_batches_association

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
    allocations: Mapped[List['Allocation']] = relationship(
        secondary=allocation_batches_association, back_populates='batches'
    )    
    # Merefaktor relasi yang dikomentari ke sintaks modern.
    # stock_movements: Mapped[List['StockMovement']] = relationship(back_populates='batch')

    ### DEVIL'S ADVOCATE NOTE ###
    # Menghapus semua properti agregat (`volume`, `total_shipped`, `last_stock`, dll.).
    # Properti ini adalah jebakan performa N+1 yang sangat serius. Mereka menyembunyikan
    # query yang mahal. Kalkulasi ini HARUS dilakukan secara eksplisit di service layer
    # menggunakan query SQL agregat (`func.sum()`) untuk performa yang dapat diprediksi.

    def __repr__(self) -> str:
        return f"<Batch(id={self.id})>"
