from pydantic import BaseModel
from typing import Optional

class DocumentTypeBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool = True
    is_mandatory: bool = False
    is_customer_visible: bool = True
    max_file_size_mb: int = 10
    allowed_extensions: Optional[str] = None
    auto_generate: bool = False
    template_path: Optional[str] = None

class DocumentTypeCreate(DocumentTypeBase):
    pass

class DocumentTypeUpdate(DocumentTypeBase):
    pass

class DocumentTypeInDBBase(DocumentTypeBase):
    id: int

    class Config:
        orm_mode = True

class DocumentType(DocumentTypeInDBBase):
    pass
