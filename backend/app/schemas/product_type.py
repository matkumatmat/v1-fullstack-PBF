from pydantic import BaseModel
from typing import Optional

class ProductTypeBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    sort_order: int = 0

class ProductTypeCreate(ProductTypeBase):
    pass

class ProductTypeUpdate(ProductTypeBase):
    pass

class ProductTypeInDBBase(ProductTypeBase):
    id: int

    class Config:
        from_attributes = True

class ProductType(ProductTypeInDBBase):
    pass
