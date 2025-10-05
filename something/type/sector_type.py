from typing import Optional
from pydantic import Field
from ..base import (_Base, _WithDbMixin, _PublicIdentifierMixin,
                    _InternalIdentifierMixin, _TimestampMixin,
                    FeResBase, FeResLookup, FePlUpdate, FePlBase,
                    DbBase, TypeUpdate, TypeBase
)
class _SectorTypeCore(TypeBase):
    default_payment_terms: Optional[int] = None
    default_delivery_terms: Optional[str] = Field(default=None, max_length=50)

class SectorTypeFePl(TypeBase, _SectorTypeCore, FePlBase):
    pass

class SectorTypeFePlUpdate(TypeUpdate):
    default_payment_terms: Optional[int] = None
    default_delivery_terms: Optional[str] = None

class SectorTypeFeResLookup(FeResLookup):
    code: str
    color_code: str

class SectorTypeDb(_SectorTypeCore, DbBase, TypeBase):
    pass