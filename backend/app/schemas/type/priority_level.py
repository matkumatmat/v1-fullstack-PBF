# file: app/schemas/type/priority_level.py

from typing import Optional
from pydantic import Field
from .base import TypeBase, TypeCreate, TypeUpdate, TypeInDBBase
from datetime import date, datetime  # ✅ FIXED: Import specific classes, not module

class PriorityLevelBase(TypeBase):
    is_active: bool = Field(default=True)
    level: int = Field(..., description="Priority level, where 1 is the highest.")
    sla_hours: Optional[int] = None
    escalation_hours: Optional[int] = None
    color_code: Optional[str] = Field(default=None, max_length=7)
    icon: Optional[str] = Field(default=None, max_length=50)

class PriorityLevelCreate(TypeCreate, PriorityLevelBase):
    pass

class PriorityLevelUpdate(TypeUpdate):
    is_active: Optional[bool] = None
    level: Optional[int] = None
    sla_hours: Optional[int] = None
    escalation_hours: Optional[int] = None
    color_code: Optional[str] = None
    icon: Optional[str] = None

class PriorityLevel(TypeInDBBase, PriorityLevelBase):
    pass