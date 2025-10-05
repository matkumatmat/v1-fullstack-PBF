from __future__ import annotations
import uuid
from typing import List, Optional
from pydantic import Field
from app.schema.base import FePlBase, FeResBase, FeResLookup
from app.models.users import CustomerTypeEnum

class LocationCreate(FePlBase):
    """
    SKEMA DASAR: Membuat satu Location baru.
    """
    name: str = Field(..., max_length=150)
    location_type: Optional[str] = Field(None, max_length=50)
    country: str = Field("Indonesia", max_length=50)
    state_province: str = Field(..., max_length=50)
    postal_code: Optional[str] = Field(None, max_length=15)
    city: str = Field(..., max_length=50)
    addr_line_1: Optional[str] = Field(..., max_length=200)
    addr_line_2: Optional[str] = Field(..., max_length=200)
    addr_line_3: Optional[str] = Field(..., max_length=200)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    is_default :bool = False
    is_active :bool = True
    location_pic : Optional[str] = Field(..., max_length=20)
    location_pic_contact : Optional[str] = Field(..., max_length=15)
    minimal_order_value: Optional[float] = Field(0.0, ge=0)
    delivery_instructions: Optional[str] = Field(..., max_length=200)
    
class BranchNestedCreate(FePlBase):
    """
    SKEMA DASAR: Membuat satu Branch baru, bisa berisi Location dan anak Branch.
    """
    name: str = Field(..., max_length=150)
    locations: List[LocationCreate] = Field(default_factory=list, min_items=1, description="Setiap branch baru harus punya minimal satu lokasi.")
    children: List[BranchNestedCreate] = Field(default_factory=list)

class CustomerDetailsCreate(FePlBase):
    """SKEMA DASAR: Detail finansial Customer. Bagian dari payload input."""
    npwp: Optional[str] = Field(None, max_length=25)
    bank: Optional[str] = Field(None, max_length=100)
    rekening: Optional[str] = Field(None, max_length=50)

class CustomerSpecificationCreate(FePlBase):
    """SKEMA DASAR: Spesifikasi komersial Customer. Bagian dari payload input."""
    default_credit_limit: float = Field(0.0, ge=0)
    current_credit_limit: Optional[float] = Field(None, ge=0)
    default_payment_terms_days: int = Field(30, ge=0)

class CustomerOnboard(FePlBase):
    """
    PAYLOAD untuk endpoint `POST /customers/onboard`
    """
    name: str = Field(..., max_length=100)
    customer_type: CustomerTypeEnum
    details: CustomerDetailsCreate
    specification: CustomerSpecificationCreate
    branches: List[BranchNestedCreate] = Field(default_factory=list)

class BranchCreateForExistingCustomer(FePlBase):
    """
    PAYLOAD untuk endpoint `POST /customers/{customer_public_id}/branches`
    Mewarisi FePlBase.
    """
    branch_data: BranchNestedCreate

class CustomerCreateSimple(FePlBase):
    """
    PAYLOAD untuk endpoint `POST /customers`
    Mewarisi FePlBase.
    """
    name: str = Field(..., max_length=100)
    customer_type: CustomerTypeEnum
    details: CustomerDetailsCreate
    specification: CustomerSpecificationCreate

# =============================================================================
# BLOCK 3: SKEMA RESPONSE (OUTPUT DARI API)
# FeResBase sudah punya public_id, created_at, updated_at, dan config from_attributes.
# =============================================================================

class LocationResponse(FeResBase):
    """
    Mewarisi FeResBase untuk mendapatkan public_id, timestamps, dan ORM mode.
    """
    name: Optional[str]
    location_type: Optional[str]
    country: Optional[str]
    state_province:Optional[str]
    postal_code:Optional[str]
    city: Optional[str]
    addr_line_1: Optional[str]
    addr_line_2: Optional[str]
    addr_line_3: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]
    is_default : bool
    is_active :bool
    location_pic: Optional[str]
    location_pic_contact:Optional[str]
    minimal_order_value : Optional[float]
    delivery_instructions: Optional[str]

class BranchResponse(FeResBase):
    """
    SKEMA RESPONSE: Data satu Branch, bisa nested.
    """
    name: str
    # parent_public_id perlu diisi manual di service layer jika dibutuhkan
    locations: List[LocationResponse] = []
    children: List[BranchResponse] = []

class CustomerResponse(FeResBase):
    """
    SKEMA RESPONSE: Data dasar Customer.
    Mewarisi FeResBase.
    """
    name: str
    customer_type: CustomerTypeEnum

class CustomerWithDetailsResponse(CustomerResponse):
    """SKEMA RESPONSE: Customer dengan detail finansial & spesifikasi."""
    details: CustomerDetailsCreate # Bisa bikin response schema terpisah jika perlu
    specification: CustomerSpecificationCreate # Bisa bikin response schema terpisah jika perlu

class CustomerWithBranchesResponse(CustomerWithDetailsResponse):
    """SKEMA RESPONSE: Customer lengkap dengan seluruh hierarki branch-nya."""
    branches: List[BranchResponse] = []

class LocationLookup(FeResLookup):
    """Skema lookup enteng untuk Location. Cuma public_id dan name."""
    # public_id dan name udah diwarisin dari FeResLookup
    location_type: Optional[str]

class BranchLookup(FeResLookup):
    """Skema lookup enteng untuk Branch. Bisa nested."""
    # public_id dan name udah diwarisin dari FeResLookup
    locations: List[LocationLookup] = []
    children: List[BranchLookup] = []

class CustomerLookup(FeResLookup):
    """Skema lookup enteng untuk Customer. Isinya hierarki branch."""
    # public_id dan name udah diwarisin dari FeResLookup
    branches: List[BranchLookup] = []    