# file: app/models/order_process/contract.py (REVISED & RECOMMENDED)

import uuid
from datetime import date, datetime
from sqlalchemy import (
    Integer, String, ForeignKey, Date, Numeric, DateTime,
    func
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

from ..configuration import BaseModel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..product import Allocation, Product, Batch
    from ..order_process import SalesOrder

class TenderContract(BaseModel):
    """
    Model Master Data untuk Perjanjian Kontrak Tender.
    Menyimpan informasi tingkat tinggi tentang sebuah kontrak.
    """
    __tablename__ = 'tender_contracts'
    
    # Contract details
    contract_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    contract_date: Mapped[date] = mapped_column(Date, nullable=False)
    contract_value: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    
    # Contract period
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    # Tender information
    tender_reference: Mapped[Optional[str]] = mapped_column(String(100))
    tender_winner: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default='ACTIVE')
    
    # ERP Integration
    erp_contract_id: Mapped[Optional[str]] = mapped_column(String(50))
    erp_sync_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    # Document references
    contract_document_url: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Tracking
    created_by: Mapped[Optional[str]] = mapped_column(String(50))
    
    # --- Relationships ---
    
    # Relasi utama: Satu kontrak memiliki banyak catatan reservasi.
    contract_reservations: Mapped[List['ContractReservation']] = relationship(back_populates='contract')
    
    # Relasi sekunder: Satu kontrak bisa menghasilkan banyak Sales Order.
    sales_orders: Mapped[List['SalesOrder']] = relationship(back_populates='tender_contract')
    
    # NOTE: Relasi 'allocations' dipertimbangkan untuk dihapus karena alur yang lebih
    # akurat adalah melalui ContractReservation. Jika dipertahankan, pastikan ada
    # `tender_contract_id` di model Allocation.
    # allocations: Mapped[List['Allocation']] = relationship(back_populates='tender_contract')

    def __repr__(self) -> str:
        return f'<TenderContract {self.contract_number}>'

class ContractReservation(BaseModel):
    """
    Model Transaksional untuk mencatat setiap kuantitas stok yang
    dicadangkan untuk sebuah kontrak tender.
    """
    __tablename__ = 'contract_reservations'
    
    # --- Foreign Keys ---
    contract_id: Mapped[int] = mapped_column(ForeignKey('tender_contracts.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    batch_id: Mapped[int] = mapped_column(ForeignKey('batches.id'), nullable=False)
    allocation_id: Mapped[int] = mapped_column(ForeignKey('allocations.id'), nullable=False, unique=True) # Satu reservasi per alokasi tender
    
    # --- Reserved Quantities ---
    # Jumlah yang dicadangkan saat re-alokasi awal.
    reserved_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    # Jumlah yang sudah ditarik dari reservasi ini untuk Sales Order. Diupdate oleh service lain.
    allocated_quantity: Mapped[int] = mapped_column(Integer, default=0)
    # Sisa yang tersedia dalam reservasi ini. Diupdate oleh service lain.
    remaining_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # --- Relationships ---
    contract: Mapped['TenderContract'] = relationship(back_populates='contract_reservations')
    product: Mapped['Product'] = relationship()
    batch: Mapped['Batch'] = relationship()
    allocation: Mapped['Allocation'] = relationship()
    
    def __repr__(self) -> str:
        return f'<ContractReservation contract_id={self.contract_id} allocation_id={self.allocation_id}>'