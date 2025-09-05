from pydantic import BaseModel
from typing import Optional

class PackageTypeBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    is_fragile: bool = False
    is_stackable: bool = True
    max_stack_height: Optional[int] = None
    special_handling_required: bool = False
    handling_instructions: Optional[str] = None

class PackageTypeCreate(PackageTypeBase):
    pass

class PackageTypeUpdate(PackageTypeBase):
    pass

class PackageTypeInDBBase(PackageTypeBase):
    id: int

    class Config:
        from_attributes = True

class PackageType(PackageTypeInDBBase):
    pass
