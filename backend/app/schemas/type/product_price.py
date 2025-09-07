# file: app/schemas/type/product_price.py
import uuid
from typing import Optional
from decimal import Decimal
from datetime import date
from pydantic import Field, BaseModel, ConfigDict
import uuid
from datetime import date, datetime  # ✅ FIXED: Import specific classes, not module

# DEVIL'S ADVOCATE NOTE: Model ini tidak punya `code` dan `name` yang konsisten, jadi tidak bisa mewarisi TypeBase.
# Kita buat skema kustom untuknya.

class ProductPriceBase(BaseModel):
    product_id: int
    effective_date: date
    code: str = Field(..., max_length=50)
    name: Optional[str] = Field(default=None, max_length=100)
    HNA: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)
    HJP: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)
    HET: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)

class ProductPriceCreate(ProductPriceBase):
    pass

class ProductPriceUpdate(BaseModel):
    product_id: Optional[int] = None
    effective_date: Optional[date] = None
    code: Optional[str] = None
    name: Optional[str] = None
    HNA: Optional[Decimal] = None
    HJP: Optional[Decimal] = None
    HET: Optional[Decimal] = None

class ProductPrice(ProductPriceBase):
    id: int
    public_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)