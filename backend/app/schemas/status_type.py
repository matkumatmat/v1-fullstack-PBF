from pydantic import BaseModel
from typing import Optional

class StatusTypeBase(BaseModel):
    entity_type: str
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool = True
    is_initial_status: bool = False
    is_final_status: bool = False
    is_error_status: bool = False
    sort_order: int = 0
    color_code: Optional[str] = None
    icon: Optional[str] = None
    css_class: Optional[str] = None
    auto_transition_after_hours: Optional[int] = None
    requires_approval: bool = False
    sends_notification: bool = False

class StatusTypeCreate(StatusTypeBase):
    pass

class StatusTypeUpdate(StatusTypeBase):
    pass

class StatusTypeInDBBase(StatusTypeBase):
    id: int

    class Config:
        from_attributes = True

class StatusType(StatusTypeInDBBase):
    pass
