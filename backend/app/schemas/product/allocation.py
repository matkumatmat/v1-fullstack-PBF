# file: app/schemas/product/allocation.py

import uuid
from datetime import date, datetime
from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated

from app.models.enums import AllocationStatusEnum
from ..type.allocation_type import AllocationType
if TYPE_CHECKING:
    from ..customer.customer import Customer
    from ..warehouse.stock_placement import StockPlacement
    from .batch import Batch

# --- Allocation Schemas ---

class AllocationBase(BaseModel):
    """Skema dasar dengan field yang dapat diinput oleh pengguna untuk Allocation."""
    batch_id: int
    allocation_type_id: int
    allocated_quantity: Annotated[int, Field(..., gt=0, description="Allocated quantity must be positive.")]
    allocation_date: date
    customer_id: Optional[int] = None
    allocation_number: Optional[Annotated[str, Field(max_length=50)]] = None
    expiry_date: Optional[date] = None
    priority_level: int = Field(default=5)
    special_instructions: Optional[str] = None
    handling_requirements: Optional[str] = None
    unit_cost: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    total_value: Optional[Decimal] = Field(None, max_digits=15, decimal_places=2)
    original_reserved_quantity: int = Field(default=0)
    customer_allocated_quantity: int = Field(default=0)

class AllocationCreate(AllocationBase):
    """Skema untuk membuat Allocation baru."""
    pass

class AllocationUpdate(BaseModel):
    """Skema untuk memperbarui Allocation. Semua field opsional."""
    batch_id: Optional[int] = None
    allocation_type_id: Optional[int] = None
    allocated_quantity: Optional[Annotated[int, Field(gt=0)]] = None
    allocation_date: Optional[date] = None
    customer_id: Optional[int] = None
    allocation_number: Optional[Annotated[str, Field(max_length=50)]] = None
    expiry_date: Optional[date] = None
    priority_level: Optional[int] = None
    special_instructions: Optional[str] = None
    handling_requirements: Optional[str] = None
    unit_cost: Optional[Decimal] = None
    total_value: Optional[Decimal] = None
    original_reserved_quantity: Optional[int] = None
    customer_allocated_quantity: Optional[int] = None
    
    # Field yang dikelola server, tapi mungkin perlu di-update secara manual dalam kasus tertentu
    shipped_quantity: Optional[Annotated[int, Field(ge=0)]] = None
    reserved_quantity: Optional[Annotated[int, Field(ge=0)]] = None
    status: Optional[AllocationStatusEnum] = None

class Allocation(AllocationBase):
    """Skema read untuk Allocation, termasuk field dari server dan relasi."""
    id: int
    public_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    # Field yang dikelola server
    shipped_quantity: int
    reserved_quantity: int
    status: AllocationStatusEnum

    # Relasi yang di-load
    allocation_type: Optional[AllocationType] = None
    customer: Optional['Customer'] = None
    batch: Optional['Batch'] = None # Hindari relasi kembali ke parent jika tidak perlu
    placements: List['StockPlacement'] = []

    model_config = ConfigDict(from_attributes=True)

# --- Forward Reference Rebuilding ---
# Pemanggilan model_rebuild() sekarang dipusatkan di app/schemas/__init__.py
# untuk menghindari circular imports.