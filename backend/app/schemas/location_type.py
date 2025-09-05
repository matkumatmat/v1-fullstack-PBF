from pydantic import BaseModel
from typing import Optional

class LocationTypeBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool = True
    is_storage_location: bool = True
    is_picking_location: bool = True
    is_staging_location: bool = False
    max_weight_capacity_kg: Optional[float] = None
    supports_temperature_control: bool = False
    requires_special_access: bool = False

class LocationTypeCreate(LocationTypeBase):
    pass

class LocationTypeUpdate(LocationTypeBase):
    pass

class LocationTypeInDBBase(LocationTypeBase):
    id: int

    class Config:
        orm_mode = True

class LocationType(LocationTypeInDBBase):
    pass
