from decimal import Decimal
from pydantic import Field
from typing import Optional
from ..base import (_Base, _WithDbMixin, _PublicIdentifierMixin,
                    _InternalIdentifierMixin, _TimestampMixin,
                    FeResBase, FeResLookup, FePlUpdate, FePlBase,
                    DbBase, TypeUpdate, TypeBase
)

class _PackagingMaterialCore(TypeBase):
    material_type: Optional[str] = Field(default=None, max_length=20)
    is_reusable: bool = Field(default=False)
    is_fragile_protection: bool = Field(default=False)
    is_temperature_protection: bool = Field(default=False)
    length_cm: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    width_cm: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    height_cm: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    weight_g: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    cost_per_unit: Optional[Decimal] = Field(default=None, max_digits=8, decimal_places=2)

class PackagingMaterialFePl(TypeBase, FePlBase, _PackagingMaterialCore):
    pass

class PackagingMaterialFePlUpdate(TypeUpdate):
    material_type: Optional[str] = None
    is_reusable: Optional[bool] = None
    is_fragile_protection: Optional[bool] = None
    is_temperature_protection: Optional[bool] = None
    length_cm: Optional[Decimal] = None
    width_cm: Optional[Decimal] = None
    height_cm: Optional[Decimal] = None
    weight_g: Optional[Decimal] = None
    cost_per_unit: Optional[Decimal] = None

class PackagingMaterialFeRes(_PackagingMaterialCore, FeResBase, TypeBase):
    pass

class PackagingMaterialFeResLookup(FeResLookup):
    code: str
    name: str
    cost_per_unit : Decimal

class PackagingMaterialDb(_PackagingMaterialCore, DbBase, TypeBase):
    pass

class PackagingFragileFeRes(FeResLookup):
    is_fragile_protection: bool = Field(default=True)
    is_temperature_protection:  bool = Field(default=False)
    length_cm: Optional[Decimal] = None
    width_cm: Optional[Decimal] = None
    height_cm: Optional[Decimal] = None
    weight_g: Optional[Decimal] = None
    cost_per_unit: Optional[Decimal] = None

class PackagingTemperatureFeRes(FeResLookup):
    is_fragile_protection: bool = Field(default=False)
    is_temperature_protection:  bool = Field(default=True)
    length_cm: Optional[Decimal] = None
    width_cm: Optional[Decimal] = None
    height_cm: Optional[Decimal] = None
    weight_g: Optional[Decimal] = None
    cost_per_unit: Optional[Decimal] = None
    