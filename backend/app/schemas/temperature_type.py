from pydantic import BaseModel
from typing import Optional

class TemperatureTypeBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    min_celsius: Optional[float] = None
    max_celsius: Optional[float] = None
    optimal_celsius: Optional[float] = None
    celsius_display: Optional[str] = None
    humidity_range: Optional[str] = None
    special_storage_requirements: Optional[str] = None
    color_code: Optional[str] = None
    icon: Optional[str] = None

class TemperatureTypeCreate(TemperatureTypeBase):
    pass

class TemperatureTypeUpdate(TemperatureTypeBase):
    pass

class TemperatureTypeInDBBase(TemperatureTypeBase):
    id: int

    class Config:
        from_attributes = True

class TemperatureType(TemperatureTypeInDBBase):
    pass
