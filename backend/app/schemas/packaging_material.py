from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class PackagingMaterialBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool = True
    material_type: Optional[str] = None
    is_reusable: bool = False
    is_fragile_protection: bool = False
    is_temperature_protection: bool = False
    length_cm: Optional[float] = None
    width_cm: Optional[float] = None
    height_cm: Optional[float] = None
    weight_g: Optional[float] = None
    cost_per_unit: Optional[Decimal] = Field(None, max_digits=8, decimal_places=2)

class PackagingMaterialCreate(PackagingMaterialBase):
    pass

class PackagingMaterialUpdate(PackagingMaterialBase):
    pass

class PackagingMaterialInDBBase(PackagingMaterialBase):
    id: int

    class Config:
        from_attributes = True

class PackagingMaterial(PackagingMaterialInDBBase):
    pass
