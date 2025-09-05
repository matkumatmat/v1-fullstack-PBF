from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import date

class ProductPriceBase(BaseModel):
    code: str
    name: Optional[str] = None
    product_id: int
    effective_date: date
    HNA: Optional[Decimal] = Field(None, max_digits=15, decimal_places=2)
    HJP: Optional[Decimal] = Field(None, max_digits=15, decimal_places=2)
    HET: Optional[Decimal] = Field(None, max_digits=15, decimal_places=2)

class ProductPriceCreate(ProductPriceBase):
    pass

class ProductPriceUpdate(ProductPriceBase):
    pass

class ProductPriceInDBBase(ProductPriceBase):
    id: int

    class Config:
        from_attributes = True

class ProductPrice(ProductPriceInDBBase):
    pass
