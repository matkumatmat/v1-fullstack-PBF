# file: app/schemas/type/product_type.py

from typing import Optional
from pydantic import Field
from .base import TypeBase, TypeCreate, TypeUpdate, TypeInDBBase
from datetime import date, datetime  # ✅ FIXED: Import specific classes, not module

class ProductTypeBase(TypeBase):
    sort_order: int = Field(default=0)

class ProductTypeCreate(TypeCreate, ProductTypeBase):
    pass

class ProductTypeUpdate(TypeUpdate):
    sort_order: Optional[int] = None

class ProductType(TypeInDBBase, ProductTypeBase):
    pass