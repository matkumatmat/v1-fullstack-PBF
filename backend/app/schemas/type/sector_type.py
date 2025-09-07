# file: app/schemas/type/sector_type.py

from typing import Optional
from pydantic import Field
from .base import TypeBase, TypeCreate, TypeUpdate, TypeInDBBase

class SectorTypeBase(TypeBase):
    is_active: bool = Field(default=True)
    requires_special_handling: bool = Field(default=False)
    default_payment_terms: Optional[int] = None
    default_delivery_terms: Optional[str] = Field(default=None, max_length=50)
    requires_temperature_monitoring: bool = Field(default=False)
    requires_chain_of_custody: bool = Field(default=False)
    special_documentation: Optional[str] = None

class SectorTypeCreate(TypeCreate, SectorTypeBase):
    pass

class SectorTypeUpdate(TypeUpdate):
    is_active: Optional[bool] = None
    requires_special_handling: Optional[bool] = None
    default_payment_terms: Optional[int] = None
    default_delivery_terms: Optional[str] = None
    requires_temperature_monitoring: Optional[bool] = None
    requires_chain_of_custody: Optional[bool] = None
    special_documentation: Optional[str] = None

class SectorType(TypeInDBBase, SectorTypeBase):
    pass