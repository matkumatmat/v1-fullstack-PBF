# file: app/schemas/type/document_type.py

from typing import Optional
from pydantic import Field
from .base import TypeBase, TypeCreate, TypeUpdate, TypeInDBBase
from datetime import date, datetime  # ✅ FIXED: Import specific classes, not module

class DocumentTypeBase(TypeBase):
    is_active: bool = Field(default=True)
    is_mandatory: bool = Field(default=False)
    is_customer_visible: bool = Field(default=True)
    max_file_size_mb: int = Field(default=10)
    allowed_extensions: Optional[str] = Field(default=None, description="e.g., 'pdf,jpg,png'")
    auto_generate: bool = Field(default=False)
    template_path: Optional[str] = None

class DocumentTypeCreate(TypeCreate, DocumentTypeBase):
    pass

class DocumentTypeUpdate(TypeUpdate):
    is_active: Optional[bool] = None
    is_mandatory: Optional[bool] = None
    is_customer_visible: Optional[bool] = None
    max_file_size_mb: Optional[int] = None
    allowed_extensions: Optional[str] = None
    auto_generate: Optional[bool] = None
    template_path: Optional[str] = None

class DocumentType(TypeInDBBase, DocumentTypeBase):
    pass