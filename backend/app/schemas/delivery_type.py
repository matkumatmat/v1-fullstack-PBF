from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class DeliveryTypeBase(BaseModel):
    name: str
    description: Optional[str] = None
    estimated_days: Optional[int] = None
    cost_per_kg: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    cost_per_km: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    is_active: bool = True

class DeliveryTypeCreate(DeliveryTypeBase):
    pass

class DeliveryTypeUpdate(DeliveryTypeBase):
    pass

class DeliveryTypeInDBBase(DeliveryTypeBase):
    id: int

    class Config:
        orm_mode = True

class DeliveryType(DeliveryTypeInDBBase):
    pass
