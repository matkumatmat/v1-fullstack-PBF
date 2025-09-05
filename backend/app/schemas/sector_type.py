from pydantic import BaseModel
from typing import Optional

class SectorTypeBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool = True
    requires_special_handling: bool = False
    default_payment_terms: Optional[int] = None
    default_delivery_terms: Optional[str] = None
    requires_temperature_monitoring: bool = False
    requires_chain_of_custody: bool = False
    special_documentation: Optional[str] = None

class SectorTypeCreate(SectorTypeBase):
    pass

class SectorTypeUpdate(SectorTypeBase):
    pass

class SectorTypeInDBBase(SectorTypeBase):
    id: int

    class Config:
        orm_mode = True

class SectorType(SectorTypeInDBBase):
    pass
