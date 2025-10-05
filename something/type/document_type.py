from typing import Optional
from decimal import Decimal
from pydantic import Field
from ..base import (_Base, _WithDbMixin, _PublicIdentifierMixin,
                    _InternalIdentifierMixin, _TimestampMixin,
                    FeResBase, FeResLookup, FePlUpdate, FePlBase,
                    DbBase, TypeUpdate, TypeBase
)

class _DocumentTypeCore(TypeBase):
    is_customer_visible : Optional[int]
    max_file_size_mb: Optional[Decimal]
    allowed_extensions: Optional[bool]
    template_path: Optional[str]

class DocumentTypeFePl(TypeBase, _DocumentTypeCore, FePlBase):
    pass

class DocumentTypeFePlUpdate(TypeUpdate):
    is_customer_visible : Optional[int]
    max_file_size_mb: Optional[Decimal]
    allowed_extensions: Optional[bool]
    template_path: Optional[str]

class  DocumentTypeFeRes(_DocumentTypeCore, FeResBase, TypeBase):
    pass

class DocumentTypeFeResLookup(FeResLookup):
    code: str
    name : str

class DocumentTypeDb(_DocumentTypeCore, DbBase, TypeBase)    :
    pass




