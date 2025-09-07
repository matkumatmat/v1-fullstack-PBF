# file: app/schemas/type/customer_type.py

from typing import Optional
from decimal import Decimal
from pydantic import Field
from .base import TypeBase, TypeCreate, TypeUpdate, TypeInDBBase
from datetime import date, datetime  # ✅ FIXED: Import specific classes, not module


class CustomerTypeBase(TypeBase):
    is_active: bool = Field(default=True)
    allows_tender_allocation: bool = Field(default=False)
    requires_pre_approval: bool = Field(default=False)
    default_credit_limit: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)
    default_discount_percent: Optional[Decimal] = Field(default=None, max_digits=5, decimal_places=2)
    default_payment_terms_days: Optional[int] = Field(default=30)

class CustomerTypeCreate(TypeCreate, CustomerTypeBase):
    pass

class CustomerTypeUpdate(TypeUpdate):
    is_active: Optional[bool] = None
    allows_tender_allocation: Optional[bool] = None
    requires_pre_approval: Optional[bool] = None
    default_credit_limit: Optional[Decimal] = None
    default_discount_percent: Optional[Decimal] = None
    default_payment_terms_days: Optional[int] = None

class CustomerType(TypeInDBBase, CustomerTypeBase):
    pass