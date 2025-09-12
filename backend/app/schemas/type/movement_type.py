# file: app/schemas/type/movement_type.py

from typing import Optional
from pydantic import Field
from .base import TypeBase, TypeCreate, TypeUpdate, TypeInDBBase
from app.models.configuration import MovementDirectionEnum
from datetime import date, datetime  # ✅ FIXED: Import specific classes, not module

class MovementTypeBase(TypeBase):
    direction: MovementDirectionEnum
    auto_generate_document: bool = Field(default=False)
    document_prefix: Optional[str] = Field(default=None, max_length=10)

class MovementTypeCreate(TypeCreate, MovementTypeBase):
    pass

class MovementTypeUpdate(TypeUpdate):
    direction: Optional[MovementDirectionEnum] = None
    auto_generate_document: Optional[bool] = None
    document_prefix: Optional[str] = None

class MovementType(TypeInDBBase, MovementTypeBase):
    pass