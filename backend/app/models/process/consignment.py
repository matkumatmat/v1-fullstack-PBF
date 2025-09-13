# file: app/models/process/consignment.py (REFACTORED TO MODERN SYNTAX)

from datetime import date, datetime
from sqlalchemy import (
    Integer, String, ForeignKey, Text, Date, Numeric, Boolean,
    Enum as SQLAlchemyEnum, Table, DateTime, func
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

# ✅ FIXED: Mengimpor BaseModel yang benar dari modul configuration
from ..configuration import BaseModel

# ✅ FIXED: Menggunakan TYPE_CHECKING untuk semua referensi silang
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..users import Customer
    from ..product import Allocation, Product, Batch
    # Asumsi model Shipment akan ada di masa depan
    # from ..shipment import Shipment 

# --- Consignment Agreement (Master Data) ---

class ConsignmentAgreement(BaseModel):
    """
    Model untuk Perjanjian Konsinyasi dengan Customer.
    Direfaktor ke sintaks modern SQLAlchemy.
    """
    __tablename__ = 'consignment_agreements'
    
    agreement_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    
    # Customer information
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=False)
    
    # Agreement details
    agreement_date: Mapped[date] = mapped_column(Date, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    
    # Terms and conditions
    commission_rate: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))
    payment_terms_days: Mapped[int] = mapped_column(Integer, default=30)
    return_policy_days: Mapped[int] = mapped_column(Integer, default=90)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default='ACTIVE')
    
    # Document references
    contract_document_url: Mapped[Optional[str]] = mapped_column(String(255))
    terms_document_url: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Tracking
    created_by: Mapped[Optional[str]] = mapped_column(String(50))
    approved_by: Mapped[Optional[str]] = mapped_column(String(50))
    approved_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # --- Relationships ---
    customer: Mapped['Customer'] = relationship(back_populates='consignment_agreements')
    consignments: Mapped[List['Consignment']] = relationship(back_populates='agreement')
    statements: Mapped[List['ConsignmentStatement']] = relationship(back_populates='agreement')

    def __repr__(self) -> str:
        return f'<ConsignmentAgreement {self.agreement_number}>'

# --- Consignment Process (Transactional Models) ---

class Consignment(BaseModel):
    """
    Model untuk satu pengiriman konsinyasi.
    """
    __tablename__ = 'consignments'
    
    consignment_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    
    # Foreign Keys
    agreement_id: Mapped[int] = mapped_column(ForeignKey('consignment_agreements.id'), nullable=False)
    allocation_id: Mapped[int] = mapped_column(ForeignKey('allocations.id'), unique=True, nullable=False)
    # shipment_id: Mapped[Optional[int]] = mapped_column(ForeignKey('shipments.id'))
    
    # Details
    consignment_date: Mapped[date] = mapped_column(Date, nullable=False)
    expected_return_date: Mapped[Optional[date]] = mapped_column(Date)
    actual_return_date: Mapped[Optional[date]] = mapped_column(Date)
    
    # Financials
    total_value: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    commission_rate: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default='PENDING', nullable=False)
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)
    terms_conditions: Mapped[Optional[str]] = mapped_column(Text)
    
    # Tracking
    created_by: Mapped[Optional[str]] = mapped_column(String(50))
    shipped_by: Mapped[Optional[str]] = mapped_column(String(50))
    shipped_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # --- Relationships ---
    agreement: Mapped['ConsignmentAgreement'] = relationship(back_populates='consignments')
    allocation: Mapped['Allocation'] = relationship(back_populates='consignments')
    # shipment: Mapped[Optional['Shipment']] = relationship(back_populates='consignments')
    
    items: Mapped[List['ConsignmentItem']] = relationship(back_populates='consignment', cascade='all, delete-orphan')
    sales: Mapped[List['ConsignmentSale']] = relationship(back_populates='consignment', cascade='all, delete-orphan')
    returns: Mapped[List['ConsignmentReturn']] = relationship(back_populates='consignment', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'<Consignment {self.consignment_number}>'

class ConsignmentItem(BaseModel):
    """Detail item dalam satu pengiriman konsinyasi."""
    __tablename__ = 'consignment_items'
    
    # Foreign Keys
    consignment_id: Mapped[int] = mapped_column(ForeignKey('consignments.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    batch_id: Mapped[int] = mapped_column(ForeignKey('batches.id'), nullable=False)
    
    # Quantities
    quantity_shipped: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity_sold: Mapped[int] = mapped_column(Integer, default=0)
    quantity_returned: Mapped[int] = mapped_column(Integer, default=0)
    
    # Pricing
    unit_value: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    total_value: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    selling_price: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default='SHIPPED')
    
    # Tracking (denormalized for performance and history)
    expiry_date: Mapped[Optional[date]] = mapped_column(Date)
    lot_number: Mapped[Optional[str]] = mapped_column(String(50))
    
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # --- Relationships ---
    consignment: Mapped['Consignment'] = relationship(back_populates='items')
    product: Mapped['Product'] = relationship()
    batch: Mapped['Batch'] = relationship()

    def __repr__(self) -> str:
        return f'<ConsignmentItem id={self.id} consignment_id={self.consignment_id}>'

class ConsignmentSale(BaseModel):
    """Mencatat penjualan yang dilaporkan dari stok konsinyasi."""
    __tablename__ = 'consignment_sales'
    
    sale_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    # Foreign Keys
    consignment_id: Mapped[int] = mapped_column(ForeignKey('consignments.id'), nullable=False)
    consignment_item_id: Mapped[int] = mapped_column(ForeignKey('consignment_items.id'), nullable=False)
    
    # Details
    sale_date: Mapped[date] = mapped_column(Date, nullable=False)
    quantity_sold: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    total_value: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    
    # Commission
    commission_rate: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))
    commission_amount: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    net_amount: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    
    # End customer info
    end_customer_name: Mapped[Optional[str]] = mapped_column(String(100))
    end_customer_info: Mapped[Optional[str]] = mapped_column(Text)
    
    # Document references
    invoice_number: Mapped[Optional[str]] = mapped_column(String(50))
    receipt_document_url: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default='CONFIRMED')
    
    # Tracking
    reported_by: Mapped[Optional[str]] = mapped_column(String(50))
    reported_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    verified_by: Mapped[Optional[str]] = mapped_column(String(50))
    verified_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # --- Relationships ---
    consignment: Mapped['Consignment'] = relationship(back_populates='sales')
    consignment_item: Mapped['ConsignmentItem'] = relationship()

    def __repr__(self) -> str:
        return f'<ConsignmentSale {self.sale_number}>'

class ConsignmentReturn(BaseModel):
    """Mencatat pengembalian stok dari lokasi konsinyasi."""
    __tablename__ = 'consignment_returns'
    
    return_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    # Foreign Keys
    consignment_id: Mapped[int] = mapped_column(ForeignKey('consignments.id'), nullable=False)
    consignment_item_id: Mapped[int] = mapped_column(ForeignKey('consignment_items.id'), nullable=False)
    
    # Details
    return_date: Mapped[date] = mapped_column(Date, nullable=False)
    quantity_returned: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Reason and condition
    return_reason: Mapped[Optional[str]] = mapped_column(String(100))
    condition: Mapped[Optional[str]] = mapped_column(String(50))
    
    # QC results
    qc_status: Mapped[Optional[str]] = mapped_column(String(20))
    qc_notes: Mapped[Optional[str]] = mapped_column(Text)
    qc_by: Mapped[Optional[str]] = mapped_column(String(50))
    qc_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Disposition
    disposition: Mapped[Optional[str]] = mapped_column(String(50))
    restocked_quantity: Mapped[int] = mapped_column(Integer, default=0)
    disposed_quantity: Mapped[int] = mapped_column(Integer, default=0)
    
    # Document
    return_document_url: Mapped[Optional[str]] = mapped_column(String(255))
    photos_url: Mapped[Optional[str]] = mapped_column(Text)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default='PENDING')
    
    # Tracking
    initiated_by: Mapped[Optional[str]] = mapped_column(String(50))
    received_by: Mapped[Optional[str]] = mapped_column(String(50))
    received_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # --- Relationships ---
    consignment: Mapped['Consignment'] = relationship(back_populates='returns')
    consignment_item: Mapped['ConsignmentItem'] = relationship()

    def __repr__(self) -> str:
        return f'<ConsignmentReturn {self.return_number}>'

class ConsignmentStatement(BaseModel):
    """Model untuk laporan/statement konsinyasi periodik."""
    __tablename__ = 'consignment_statements'
    
    statement_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    # Foreign Keys
    agreement_id: Mapped[int] = mapped_column(ForeignKey('consignment_agreements.id'), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=False)
    
    # Period
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    
    # Summary totals
    total_shipped_value: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    total_sold_value: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    total_returned_value: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    total_commission: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    net_amount_due: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    
    # Payment tracking
    payment_status: Mapped[str] = mapped_column(String(20), default='PENDING')
    payment_due_date: Mapped[Optional[date]] = mapped_column(Date)
    payment_received_date: Mapped[Optional[date]] = mapped_column(Date)
    payment_amount: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    
    # Document
    statement_document_url: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default='DRAFT')
    
    # Tracking
    generated_by: Mapped[Optional[str]] = mapped_column(String(50))
    sent_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # --- Relationships ---
    agreement: Mapped['ConsignmentAgreement'] = relationship(back_populates='statements')
    customer: Mapped['Customer'] = relationship(back_populates='consignment_statements')

    def __repr__(self) -> str:
        return f'<ConsignmentStatement {self.statement_number}>'

# ✅ PENTING: Tambahkan relasi balik (back_populates) di model Customer
# Buka file app/models/users/customer.py dan tambahkan relasi ini di dalam kelas Customer:
#
# class Customer(BaseModel):
#     # ... relasi lain ...
#     consignment_agreements: Mapped[List['ConsignmentAgreement']] = relationship(back_populates='customer')
#     consignment_statements: Mapped[List['ConsignmentStatement']] = relationship(back_populates='customer')

# ✅ PENTING: Tambahkan relasi balik (back_populates) di model Allocation
# Buka file app/models/product/allocation.py dan tambahkan relasi ini di dalam kelas Allocation:
#
# class Allocation(BaseModel):
#     # ... relasi lain ...
#     consignments: Mapped[List['Consignment']] = relationship(back_populates='allocation')