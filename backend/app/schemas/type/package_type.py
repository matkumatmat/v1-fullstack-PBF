# file: app/schemas/type/package_type.py

from typing import Optional
from pydantic import Field
from .base import TypeBase, TypeCreate, TypeUpdate, TypeInDBBase
from datetime import date, datetime  # ✅ FIXED: Import specific classes, not module

class PackageTypeBase(TypeBase):
    is_fragile: bool = Field(default=False)
    is_stackable: bool = Field(default=True)
    max_stack_height: Optional[int] = None
    special_handling_required: bool = Field(default=False)
    handling_instructions: Optional[str] = None

class PackageTypeCreate(TypeCreate, PackageTypeBase):
    pass

class PackageTypeUpdate(TypeUpdate):
    is_fragile: Optional[bool] = None
    is_stackable: Optional[bool] = None
    max_stack_height: Optional[int] = None
    special_handling_required: Optional[bool] = None
    handling_instructions: Optional[str] = None

class PackageType(TypeInDBBase, PackageTypeBase):
    pass