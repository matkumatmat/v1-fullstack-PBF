# file: app/schemas/type/delivery_type.py
import uuid
from typing import Optional
from decimal import Decimal
from pydantic import Field, BaseModel, ConfigDict
import datetime

# DEVIL'S ADVOCATE NOTE: Model ini tidak punya `code`, jadi tidak bisa mewarisi TypeBase.
# Kita buat skema kustom untuknya.

class DeliveryTypeBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    estimated_days: Optional[int] = None
    cost_per_kg: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    cost_per_km: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    is_active: bool = Field(default=True)

class DeliveryTypeCreate(DeliveryTypeBase):
    pass

class DeliveryTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    estimated_days: Optional[int] = None
    cost_per_kg: Optional[Decimal] = None
    cost_per_km: Optional[Decimal] = None
    is_active: Optional[bool] = None

class DeliveryType(DeliveryTypeBase):
    id: int
    public_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)