import uuid
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr

from ...base import (
    FePlBase, FePlUpdate, FeResBase, FeResLookup, DbBase
)
from ...type import CustomerTypeFeRes, SectorTypeFeRes
from app.models.configuration import AddressTypeEnum

class _CustomerAddressCore(BaseModel):
    """Field-field inti dari sebuah CustomerAddress."""
    address_name: str = Field(..., max_length=100)
    address_type: AddressTypeEnum = AddressTypeEnum.CUSTOMER
    address_line1: str = Field(..., max_length=200)
    address_line2: Optional[str] = Field(None, max_length=200)
    city: str = Field(..., max_length=50)
    state_province: Optional[str] = Field(None, max_length=50)
    postal_code: Optional[str] = Field(None, max_length=10)
    country: str = Field("Indonesia", max_length=50)
    contact_person: Optional[str] = Field(None, max_length=100)
    contact_phone: Optional[str] = Field(None, max_length=20)
    contact_email: Optional[EmailStr] = None
    is_active: bool = True
    is_default: bool = False

class CustomerAddressFePl(_CustomerAddressCore, FePlBase):
    """
    Payload untuk MEMBUAT CustomerAddress.
    customer_public_id akan diisi oleh service saat membuat Customer secara bersarang.
    """
    pass

class CustomerAddressFePlUpdate(FePlUpdate):
    """Payload untuk MENGUBAH CustomerAddress."""
    address_name: Optional[str] = Field(None, max_length=100)
    address_type: Optional[AddressTypeEnum] = None
    address_line1: Optional[str] = Field(None, max_length=200)
    # ... tambahkan field lain yang bisa di-update ...
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None

class CustomerAddressFeRes(_CustomerAddressCore, FeResBase):
    """Respons LENGKAP untuk CustomerAddress."""
    # Tidak ada field tambahan yang spesifik, semua sudah ter-cover.
    pass

class CustomerAddressDb(_CustomerAddressCore, DbBase):
    """Representasi internal lengkap untuk CustomerAddress."""
    customer_id: int

# ===================================================================
# SKEMA UNTUK CUSTOMER
# ===================================================================

class _CustomerCore(BaseModel):
    """Field-field inti dari sebuah Customer."""
    code: str = Field(..., max_length=20)
    name: str = Field(..., max_length=100)

class CustomerFePl(_CustomerCore, FePlBase):
    """Payload untuk MEMBUAT Customer baru, bisa termasuk alamatnya."""
    customer_type_public_id: uuid.UUID
    sector_type_public_id: uuid.UUID
    # Memungkinkan pembuatan alamat secara bersamaan
    addresses: List[CustomerAddressFePl] = []

class CustomerFePlUpdate(FePlUpdate):
    """Payload untuk MENGUBAH Customer."""
    code: Optional[str] = Field(None, max_length=20)
    name: Optional[str] = Field(None, max_length=100)
    customer_type_public_id: Optional[uuid.UUID] = None
    sector_type_public_id: Optional[uuid.UUID] = None

class CustomerFeRes(_CustomerCore, FeResBase):
    """Respons LENGKAP untuk Customer, termasuk relasinya."""
    customer_type: CustomerTypeFeRes
    sector_type: SectorTypeFeRes
    addresses: List[CustomerAddressFeRes] = []
    # allocations: List['AllocationFeResSummary'] = [] # Bisa ditambahkan nanti

class CustomerFeResLookup(FeResLookup):
    """Respons RAMPING untuk lookup Customer."""
    code: str

class CustomerDb(_CustomerCore, DbBase):
    """Representasi internal lengkap untuk Customer."""
    customer_type_id: int
    sector_type_id: int
    addresses: List[CustomerAddressDb] = []
    # allocations: List['AllocationDb'] = []