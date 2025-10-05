from typing import Optional
from decimal import Decimal
from pydantic import Field
from ..base import (_Base, _WithDbMixin, _PublicIdentifierMixin,
                    _InternalIdentifierMixin, _TimestampMixin,
                    FeResBase, FeResLookup, FePlUpdate, FePlBase,
                    DbBase, TypeUpdate, TypeBase
)
class _TemperatureTypeCore(TypeBase):
    min_celsius: Optional[Decimal] = Field(default=None, max_digits=5, decimal_places=2)
    max_celsius: Optional[Decimal] = Field(default=None, max_digits=5, decimal_places=2)
    optimal_celsius: Optional[Decimal] = Field(default=None, max_digits=5, decimal_places=2)
    celsius_display: Optional[str] = Field(default=None, max_length=20)
    humidity_range: Optional[str] = Field(default=None, max_length=20)
    special_storage_requirements: Optional[str] = None
    color_code: Optional[str] = Field(default=None, max_length=7)
    icon: Optional[str] = Field(default=None, max_length=50)

class TemperatureTypeFePl(TypeBase, _TemperatureTypeCore):
    pass

class TemperatureTypeFePlUpdate(TypeUpdate):
    min_celsius: Optional[Decimal] = None
    max_celsius: Optional[Decimal] = None
    optimal_celsius: Optional[Decimal] = None
    celsius_display: Optional[str] = None
    humidity_range: Optional[str] = None
    special_storage_requirements: Optional[str] = None
    color_code: Optional[str] = None
    icon: Optional[str] = None

class TemperatureTypeFeRes(_TemperatureTypeCore, FeResBase, TypeBase):
    pass

class TemperatureTypeFeResLookup(FeResLookup):
    celsius_display: Optional[str] = None
    color_code: Optional[str] = None
    icon: Optional[str] = None     

class TemperatureTypeDb(_TemperatureTypeCore, DbBase, TypeBase):
    pass