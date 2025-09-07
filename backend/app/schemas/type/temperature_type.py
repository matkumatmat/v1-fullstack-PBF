# file: app/schemas/type/temperature_type.py

from typing import Optional
from decimal import Decimal
from pydantic import Field
from .base import TypeBase, TypeCreate, TypeUpdate, TypeInDBBase

class TemperatureTypeBase(TypeBase):
    min_celsius: Optional[Decimal] = Field(default=None, max_digits=5, decimal_places=2)
    max_celsius: Optional[Decimal] = Field(default=None, max_digits=5, decimal_places=2)
    optimal_celsius: Optional[Decimal] = Field(default=None, max_digits=5, decimal_places=2)
    celsius_display: Optional[str] = Field(default=None, max_length=20)
    humidity_range: Optional[str] = Field(default=None, max_length=20)
    special_storage_requirements: Optional[str] = None
    color_code: Optional[str] = Field(default=None, max_length=7)
    icon: Optional[str] = Field(default=None, max_length=50)

class TemperatureTypeCreate(TypeCreate, TemperatureTypeBase):
    pass

class TemperatureTypeUpdate(TypeUpdate):
    min_celsius: Optional[Decimal] = None
    max_celsius: Optional[Decimal] = None
    optimal_celsius: Optional[Decimal] = None
    celsius_display: Optional[str] = None
    humidity_range: Optional[str] = None
    special_storage_requirements: Optional[str] = None
    color_code: Optional[str] = None
    icon: Optional[str] = None

class TemperatureType(TypeInDBBase, TemperatureTypeBase):
    pass