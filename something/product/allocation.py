import uuid
from typing import Optional, List, Annotated, TYPE_CHECKING
from pydantic import BaseModel, Field
from ...base import (
    FePlBase, FePlUpdate, FeResBase, DbBase
)
from ...type import AllocationTypeFeRes
#from ..user import CustomerFeRes
from app.models.configuration import AllocationStatusEnum
if TYPE_CHECKING:
    from .batch import BatchFeRes,BatchDb

class _AllocationCore(BaseModel):
    """Field-field inti dari sebuah Allocation."""
    allocated_quantity: Annotated[int, Field(gt=0)]
    status: AllocationStatusEnum = AllocationStatusEnum.ACTIVE
    allocation_number: Optional[str] = Field(None, max_length=50)

class AllocationFePl(_AllocationCore, FePlBase):
    """Payload untuk membuat Allocation baru."""
    batch_public_ids: List[uuid.UUID] = Field(..., min_length=1)
    allocation_type_public_id: uuid.UUID
    customer_public_id: Optional[uuid.UUID] = None

class AllocationFePlUpdate(FePlUpdate):
    """Payload untuk memperbarui Allocation."""
    allocated_quantity: Optional[Annotated[int, Field(gt=0)]] = None
    status: Optional[AllocationStatusEnum] = None

class AllocationFeRes(_AllocationCore, FeResBase):
    """Respons lengkap untuk Allocation."""
    shipped_quantity: int
    reserved_quantity: int
    allocation_type: AllocationTypeFeRes
    #customer: Optional[CustomerFeRes] = None
    batches: List[BatchFeRes]

class AllocationDb(_AllocationCore, DbBase):
    """Representasi internal lengkap untuk Allocation."""
    allocation_type_id: int
    customer_id: Optional[int] = None
    batches: List[BatchDb]
    # placements: List['RackItemDb']
