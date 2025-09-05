from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class CustomerTypeBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool = True
    allows_tender_allocation: bool = False
    requires_pre_approval: bool = False
    default_credit_limit: Optional[Decimal] = Field(None, max_digits=15, decimal_places=2)
    default_discount_percent: Optional[Decimal] = Field(None, max_digits=5, decimal_places=2)
    default_payment_terms_days: int = 30

class CustomerTypeCreate(CustomerTypeBase):
    pass

class CustomerTypeUpdate(CustomerTypeBase):
    pass

class CustomerTypeInDBBase(CustomerTypeBase):
    id: int

    class Config:
        from_attributes = True

class CustomerType(CustomerTypeInDBBase):
    pass
