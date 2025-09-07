# file: app/schemas/customer/customer_address.py

import uuid
from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing_extensions import Annotated

from app.models.enums import AddressTypeEnum
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .customer import Customer

# --- CustomerAddress Schemas ---

class CustomerAddressBase(BaseModel):
    """Skema dasar dengan field yang dapat diinput oleh pengguna untuk CustomerAddress."""
    customer_id: int
    address_name: Annotated[str, Field(..., max_length=100)]
    address_type: AddressTypeEnum = Field(default=AddressTypeEnum.DELIVERY)
    address_line1: Annotated[str, Field(..., max_length=200)]
    address_line2: Optional[Annotated[str, Field(max_length=200)]] = None
    city: Annotated[str, Field(..., max_length=50)]
    state_province: Optional[Annotated[str, Field(max_length=50)]] = None
    postal_code: Optional[Annotated[str, Field(max_length=10)]] = None
    country: Annotated[str, Field(default='Indonesia', max_length=50)]
    contact_person: Optional[Annotated[str, Field(max_length=100)]] = None
    contact_phone: Optional[Annotated[str, Field(max_length=20)]] = None
    contact_email: Optional[EmailStr] = None # <-- Menggunakan tipe EmailStr untuk validasi email otomatis
    delivery_instructions: Optional[str] = None
    special_requirements: Optional[str] = None
    latitude: Optional[Decimal] = Field(None, max_digits=9, decimal_places=6)
    longitude: Optional[Decimal] = Field(None, max_digits=9, decimal_places=6)
    is_active: bool = Field(default=True)
    is_default: bool = Field(default=False)
    created_by: Optional[Annotated[str, Field(max_length=50)]] = None

class CustomerAddressCreate(CustomerAddressBase):
    """Skema untuk membuat CustomerAddress baru."""
    pass

class CustomerAddressUpdate(BaseModel):
    """Skema untuk memperbarui CustomerAddress. Semua field opsional."""
    customer_id: Optional[int] = None # Biasanya tidak diubah
    address_name: Optional[Annotated[str, Field(max_length=100)]] = None
    address_type: Optional[AddressTypeEnum] = None
    address_line1: Optional[Annotated[str, Field(max_length=200)]] = None
    address_line2: Optional[Annotated[str, Field(max_length=200)]] = None
    city: Optional[Annotated[str, Field(max_length=50)]] = None
    state_province: Optional[Annotated[str, Field(max_length=50)]] = None
    postal_code: Optional[Annotated[str, Field(max_length=10)]] = None
    country: Optional[Annotated[str, Field(max_length=50)]] = None
    contact_person: Optional[Annotated[str, Field(max_length=100)]] = None
    contact_phone: Optional[Annotated[str, Field(max_length=20)]] = None
    contact_email: Optional[EmailStr] = None
    delivery_instructions: Optional[str] = None
    special_requirements: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None
    created_by: Optional[Annotated[str, Field(max_length=50)]] = None

class CustomerAddress(CustomerAddressBase):
    """Skema read untuk CustomerAddress, termasuk field dari server."""
    id: int
    public_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    # Relasi ke parent tidak selalu perlu di-load untuk menghindari data berlebihan
    customer: Optional['Customer'] = None

    model_config = ConfigDict(from_attributes=True)

# --- Forward Reference Rebuilding ---
# Diperlukan jika skema saling mereferensikan.
#from .customer import Customer
#Customer.model_rebuild()