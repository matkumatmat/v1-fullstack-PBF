import uuid
from datetime import date, datetime
from typing import Optional, List, Annotated, TYPE_CHECKING
from pydantic import BaseModel, Field
from ...base import (
    FePlBase, FePlUpdate, FeResBase, FeResLookup, DbBase, _WithDbMixin, _PublicIdentifierMixin
)
from ...type import PackageTypeFeRes, TemperatureTypeFeRes, AllocationTypeFeRes
from app.models.configuration import AllocationStatusEnum

if TYPE_CHECKING:
    from .product import ProductFeResLookup,ProductDb
    from .allocation import AllocationDb


class _BatchCore(BaseModel):
    """Field-field inti dari sebuah Batch."""
    lot_number: str = Field(..., max_length=50)
    expiry_date: date
    NIE: str = Field(..., max_length=50)
    received_quantity: Annotated[int, Field(gt=0)]
    receipt_document: str = Field(..., max_length=25)
    receipt_date: date
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    weight: Optional[float] = None

class BatchFePl(_BatchCore, FePlBase):
    """Payload untuk membuat Batch baru."""
    product_public_id: uuid.UUID

class BatchFePlUpdate(FePlUpdate):
    """Payload untuk memperbarui Batch."""
    expiry_date: Optional[date] = None
    NIE: Optional[str] = Field(None, max_length=50)

class BatchFeRes(_BatchCore, FeResBase):
    """Respons lengkap untuk Batch."""
    product: ProductFeResLookup

class BatchDb(_BatchCore, DbBase):
    """Representasi internal lengkap untuk Batch."""
    product_id: int
    product: ProductDb
    allocations: List['AllocationDb']

class BatchSummary(_WithDbMixin, _PublicIdentifierMixin):
    """
    Representasi ringkas dari Batch, untuk ditampilkan di dalam Allocation.
    TIDAK memiliki relasi 'allocations' untuk mencegah rekursi.
    """
    lot_number: str
    expiry_date: date
    received_quantity: int