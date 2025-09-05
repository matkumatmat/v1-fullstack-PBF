from pydantic import BaseModel
from typing import Optional

class PriorityLevelBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool = True
    level: int
    sla_hours: Optional[int] = None
    escalation_hours: Optional[int] = None
    color_code: Optional[str] = None
    icon: Optional[str] = None

class PriorityLevelCreate(PriorityLevelBase):
    pass

class PriorityLevelUpdate(PriorityLevelBase):
    pass

class PriorityLevelInDBBase(PriorityLevelBase):
    id: int

    class Config:
        orm_mode = True

class PriorityLevel(PriorityLevelInDBBase):
    pass
