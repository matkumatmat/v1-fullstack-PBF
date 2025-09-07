# file: app/schemas/type/allocation_type.py

from typing import Optional
from .base import TypeBase, TypeCreate, TypeUpdate, TypeInDBBase

class AllocationTypeBase(TypeBase):
    color_code: Optional[str] = None
    icon: Optional[str] = None

class AllocationTypeCreate(TypeCreate, AllocationTypeBase):
    pass

class AllocationTypeUpdate(TypeUpdate):
    color_code: Optional[str] = None
    icon: Optional[str] = None

class AllocationType(TypeInDBBase, AllocationTypeBase):
    pass