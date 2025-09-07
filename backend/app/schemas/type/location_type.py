# file: app/schemas/type/location_type.py

from typing import Optional
from decimal import Decimal
from pydantic import Field
from .base import TypeBase, TypeCreate, TypeUpdate, TypeInDBBase

class LocationTypeBase(TypeBase):
    is_active: bool = Field(default=True)
    is_storage_location: bool = Field(default=True)
    is_picking_location: bool = Field(default=True)
    is_staging_location: bool = Field(default=False)
    max_weight_capacity_kg: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    supports_temperature_control: bool = Field(default=False)
    requires_special_access: bool = Field(default=False)

class LocationTypeCreate(TypeCreate, LocationTypeBase):
    pass

class LocationTypeUpdate(TypeUpdate):
    is_active: Optional[bool] = None
    is_storage_location: Optional[bool] = None
    is_picking_location: Optional[bool] = None
    is_staging_location: Optional[bool] = None
    max_weight_capacity_kg: Optional[Decimal] = None
    supports_temperature_control: Optional[bool] = None
    requires_special_access: Optional[bool] = None

class LocationType(TypeInDBBase, LocationTypeBase):
    pass