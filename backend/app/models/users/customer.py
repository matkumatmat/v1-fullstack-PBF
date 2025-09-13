# file: app/models/customer.py

from sqlalchemy import (
    Integer, String, ForeignKey, Text, Boolean, Numeric, Enum as SQLAlchemyEnum
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

# Impor komponen dasar dan Enum yang relevan
from ..configuration import BaseModel,AddressTypeEnum

# Impor tipe relasi untuk type hinting yang lebih baik.
# Menggunakan `__future__` import style untuk menghindari circular import issues jika diperlukan.
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..configuration import CustomerType, SectorType
    from ..order_process import SalesOrder
    from ..product import Allocation
    from ..process import ConsignmentAgreement, ConsignmentStatement

class Customer(BaseModel):
    __tablename__ = 'customers'
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    customer_type_id: Mapped[int] = mapped_column(ForeignKey('customer_types.id'), nullable=False)
    sector_type_id: Mapped[int] = mapped_column(ForeignKey('sector_types.id'), nullable=False)

    # --- Relationships ---
    customer_type: Mapped['CustomerType'] = relationship(back_populates='customers')
    sector_type: Mapped['SectorType'] = relationship(back_populates='customers')
    sales_orders: Mapped[List['SalesOrder']] = relationship(back_populates='customer')
    allocations: Mapped[List['Allocation']] = relationship(back_populates='customer')
    
    ### DEVIL'S ADVOCATE NOTE ###
    # Merefaktor relasi yang dikomentari ke sintaks modern.
    # Saat Anda siap menggunakannya, Anda hanya perlu menghapus komentar.
    consignment_agreements: Mapped[List['ConsignmentAgreement']] = relationship(back_populates='customer')
    consignment_statements: Mapped[List['ConsignmentStatement']] = relationship(back_populates='customer')    
    
    addresses: Mapped[List['CustomerAddress']] = relationship(back_populates='customer', cascade='all, delete-orphan')
    
    ### DEVIL'S ADVOCATE NOTE ###
    # Properti ini berguna untuk logika Python, tetapi tidak bisa di-query di database.
    # Ini adalah kompromi yang bisa diterima selama Anda sadar akan keterbatasannya.
    @property
    def default_address(self) -> Optional['CustomerAddress']:
        return next((addr for addr in self.addresses if addr.is_default), None)
    
    @property
    def delivery_addresses(self) -> List['CustomerAddress']:
        return [addr for addr in self.addresses if addr.address_type == AddressTypeEnum.DELIVERY and addr.is_active]    
    
    def __repr__(self) -> str:
        return f'<Customer id={self.id} code="{self.code}" name="{self.name}">'

class CustomerAddress(BaseModel):
    """Model untuk multiple addresses per customer"""
    __tablename__ = 'customer_addresses'
    
    # id, public_id, created_at, updated_at diwarisi dari BaseModel.
    # public_id = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False, index=True) # <-- DIGANTIKAN OLEH MIXIN

    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=False)
    address_name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    address_type: Mapped[AddressTypeEnum] = mapped_column(SQLAlchemyEnum(AddressTypeEnum, name="address_type_enum", create_type=False), default=AddressTypeEnum.DELIVERY)
    
    address_line1: Mapped[str] = mapped_column(String(200), nullable=False)
    address_line2: Mapped[Optional[str]] = mapped_column(String(200))
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    state_province: Mapped[Optional[str]] = mapped_column(String(50))
    postal_code: Mapped[Optional[str]] = mapped_column(String(10))
    country: Mapped[str] = mapped_column(String(50), default='Indonesia')
    contact_person: Mapped[Optional[str]] = mapped_column(String(100))
    contact_phone: Mapped[Optional[str]] = mapped_column(String(20))
    contact_email: Mapped[Optional[str]] = mapped_column(String(100))
    delivery_instructions: Mapped[Optional[str]] = mapped_column(Text)
    special_requirements: Mapped[Optional[str]] = mapped_column(Text)
    
    latitude: Mapped[Optional[float]] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Optional[float]] = mapped_column(Numeric(9, 6))
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    ### DEVIL'S ADVOCATE NOTE ###
    # Menambahkan kolom `is_default` seperti yang diimplikasikan oleh properti di model `Customer`.
    # `default=False` dan `nullable=False` adalah pilihan yang aman.
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    created_by: Mapped[Optional[str]] = mapped_column(String(50))
    
    ### DEVIL'S ADVOCATE NOTE ###
    # Kolom `created_date` ini redundan karena kita sudah memiliki `created_at` dari `BaseModel`.
    # Menghapusnya akan membuat model lebih konsisten. Sesuai permintaan, saya
    # mempertahankannya dalam bentuk komentar dengan penjelasan.
    # created_date = Column(DateTime, default=func.current_timestamp()) # <-- DIKOMENTARI: Redundan dengan `created_at` dari BaseModel. Sebaiknya dihapus untuk konsistensi.

    # --- Relationships ---
    customer: Mapped['Customer'] = relationship(back_populates='addresses')
    
    ### DEVIL'S ADVOCATE NOTE ###
    # Merefaktor relasi yang dikomentari ke sintaks modern.
    # shipments: Mapped[List['Shipment']] = relationship(back_populates='delivery_address')
    
    def __repr__(self) -> str:
        # Menggunakan `self.customer.name` dalam `__repr__` bisa memicu query tambahan jika relasi belum di-load.
        # Lebih aman menggunakan `self.customer_id` untuk representasi dasar.
        return f'<CustomerAddress id={self.id} customer_id={self.customer_id} name="{self.address_name}">'