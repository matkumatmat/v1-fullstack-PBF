import uuid
from datetime import date, datetime
from typing import Optional, List, Annotated, TYPE_CHECKING
from pydantic import BaseModel, Field
from ...base import (
    FePlBase, FePlUpdate, FeResBase, FeResLookup, DbBase
)
from ...type import ProductTypeFeRes, PackageTypeFeRes, TemperatureTypeFeRes
from models.configuration.enums import AllocationStatusEnum

if TYPE_CHECKING:
    from .batch import BatchFeRes,BatchDb

class _ProductCore(BaseModel):
    """Field-field inti dari sebuah Product."""
    product_code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=100)
    manufacturer: Optional[str] = None

class ProductFePl(_ProductCore, FePlBase):
    """Payload untuk membuat Product baru."""
    product_type_public_id: uuid.UUID
    package_type_public_id: uuid.UUID
    temperature_type_public_id: uuid.UUID

class ProductFePlUpdate(FePlUpdate):
    """Payload untuk memperbarui Product."""
    name: Optional[str] = None
    manufacturer: Optional[str] = None

class ProductFeRes(_ProductCore, FeResBase):
    """Respons lengkap untuk Product."""
    product_type: ProductTypeFeRes
    package_type: PackageTypeFeRes
    temperature_type: TemperatureTypeFeRes
    batches: List['BatchFeRes'] 

class ProductFeResLookup(FeResLookup):
    """Respons ramping untuk lookup Product. Mewarisi public_id dan name."""
    product_code: str

class ProductDb(_ProductCore, DbBase):
    """Representasi internal lengkap untuk Product."""
    product_type_id: int
    package_type_id: int
    temperature_type_id: int
    batches: List['BatchDb'] 