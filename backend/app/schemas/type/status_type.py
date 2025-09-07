# file: app/schemas/type/status_type.py

from typing import Optional
from pydantic import Field
from .base import TypeBase, TypeCreate, TypeUpdate, TypeInDBBase

class StatusTypeBase(TypeBase):
    entity_type: str = Field(..., max_length=50, description="e.g., 'SALES_ORDER', 'SHIPMENT'")
    is_active: bool = Field(default=True)
    is_initial_status: bool = Field(default=False)
    is_final_status: bool = Field(default=False)
    is_error_status: bool = Field(default=False)
    sort_order: int = Field(default=0)
    color_code: Optional[str] = Field(default=None, max_length=7)
    icon: Optional[str] = Field(default=None, max_length=50)
    css_class: Optional[str] = Field(default=None, max_length=50)
    auto_transition_after_hours: Optional[int] = None
    requires_approval: bool = Field(default=False)
    sends_notification: bool = Field(default=False)

class StatusTypeCreate(TypeCreate, StatusTypeBase):
    pass

class StatusTypeUpdate(TypeUpdate):
    entity_type: Optional[str] = None
    is_active: Optional[bool] = None
    is_initial_status: Optional[bool] = None
    is_final_status: Optional[bool] = None
    is_error_status: Optional[bool] = None
    sort_order: Optional[int] = None
    color_code: Optional[str] = None
    icon: Optional[str] = None
    css_class: Optional[str] = None
    auto_transition_after_hours: Optional[int] = None
    requires_approval: Optional[bool] = None
    sends_notification: Optional[bool] = None

class StatusType(TypeInDBBase, StatusTypeBase):
    pass