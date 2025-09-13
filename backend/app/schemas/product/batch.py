# file: app/schemas/product/batch.py

import uuid
from datetime import date, datetime
from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict, conint
from typing import Annotated

# ✅ FIXED: Use TYPE_CHECKING for circular references
if TYPE_CHECKING:
    from .product import Product
    from .allocation import Allocation
    from .product import ProductInBatch

# --- Batch Schemas ---

class BatchBase(BaseModel):
    """Skema dasar dengan field yang dapat diinput oleh pengguna untuk Batch."""
    lot_number: Annotated[str, Field(..., max_length=50)]
    expiry_date: date
    NIE: Annotated[str, Field(..., max_length=50)]
    received_quantity: Annotated[int, Field(gt=0, description="Quantity received must be positive.")]
    receipt_document: Annotated[str, Field(str, max_length=25)]
    receipt_date: date
    receipt_pic: Optional[Annotated[str, Field(max_length=25)]] = None
    receipt_doc_url: Optional[Annotated[str, Field(max_length=255)]] = None
    length: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    width: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    height: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    weight: Optional[Decimal] = Field(None, max_digits=10, decimal_places=3)
    product_id: int

class BatchCreate(BatchBase):
    """Skema untuk membuat Batch baru."""
    pass

class BatchUpdate(BaseModel):
    """Skema untuk memperbarui Batch. Semua field opsional."""
    lot_number: Optional[Annotated[str, Field(max_length=50)]] = None
    expiry_date: Optional[date] = None
    NIE: Optional[Annotated[str, Field(max_length=50)]] = None
    received_quantity: Optional[Annotated[int, Field(gt=0)]] = None
    receipt_document: Optional[Annotated[str, Field(max_length=25)]] = None
    receipt_date: Optional[date] = None
    receipt_pic: Optional[Annotated[str, Field(max_length=25)]] = None
    receipt_doc_url: Optional[Annotated[str, Field(max_length=255)]] = None
    length: Optional[Decimal] = None
    width: Optional[Decimal] = None
    height: Optional[Decimal] = None
    weight: Optional[Decimal] = None
    # product_id biasanya tidak diubah, tapi bisa diaktifkan jika perlu
    product_id: Optional[int] = None

class Batch(BatchBase):
    """Skema read untuk Batch, termasuk field dari server dan relasi."""
    id: int
    public_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    # Relasi yang di-load
    #product: Optional['ProductInBatch'] = None
    allocations: List['Allocation'] = []

    model_config = ConfigDict(from_attributes=True)