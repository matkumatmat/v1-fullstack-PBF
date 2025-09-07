# file: app/schemas/type/packaging_material.py

from typing import Optional
from decimal import Decimal
from pydantic import Field
from .base import TypeBase, TypeCreate, TypeUpdate, TypeInDBBase
from datetime import date, datetime  # ✅ FIXED: Import specific classes, not module

class PackagingMaterialBase(TypeBase):
    is_active: bool = Field(default=True)
    material_type: Optional[str] = Field(default=None, max_length=20)
    is_reusable: bool = Field(default=False)
    is_fragile_protection: bool = Field(default=False)
    is_temperature_protection: bool = Field(default=False)
    length_cm: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    width_cm: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    height_cm: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    weight_g: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    cost_per_unit: Optional[Decimal] = Field(default=None, max_digits=8, decimal_places=2)

class PackagingMaterialCreate(TypeCreate, PackagingMaterialBase):
    pass

class PackagingMaterialUpdate(TypeUpdate):
    is_active: Optional[bool] = None
    material_type: Optional[str] = None
    is_reusable: Optional[bool] = None
    is_fragile_protection: Optional[bool] = None
    is_temperature_protection: Optional[bool] = None
    length_cm: Optional[Decimal] = None
    width_cm: Optional[Decimal] = None
    height_cm: Optional[Decimal] = None
    weight_g: Optional[Decimal] = None
    cost_per_unit: Optional[Decimal] = None

class PackagingMaterial(TypeInDBBase, PackagingMaterialBase):
    pass