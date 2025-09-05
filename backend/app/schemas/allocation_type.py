from pydantic import BaseModel
from typing import Optional

class AllocationTypeBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    color_code: Optional[str] = None
    icon: Optional[str] = None

class AllocationTypeCreate(AllocationTypeBase):
    pass

class AllocationTypeUpdate(AllocationTypeBase):
    pass

class AllocationTypeInDBBase(AllocationTypeBase):
    id: int

    class Config:
        orm_mode = True

class AllocationType(AllocationTypeInDBBase):
    pass
