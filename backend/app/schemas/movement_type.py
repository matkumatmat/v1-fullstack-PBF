from pydantic import BaseModel
from typing import Optional

class MovementTypeBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    direction: str
    auto_generate_document: bool = False
    document_prefix: Optional[str] = None

class MovementTypeCreate(MovementTypeBase):
    pass

class MovementTypeUpdate(MovementTypeBase):
    pass

class MovementTypeInDBBase(MovementTypeBase):
    id: int

    class Config:
        from_attributes = True

class MovementType(MovementTypeInDBBase):
    pass
