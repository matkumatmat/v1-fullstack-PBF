from typing import Optional
from pydantic import Field
from ..base import (_Base, _WithDbMixin, _PublicIdentifierMixin,
                    _InternalIdentifierMixin, _TimestampMixin,
                    FeResBase, FeResLookup, FePlUpdate, FePlBase,
                    DbBase, TypeUpdate, TypeBase
)
class _PackageTypeCore(TypeBase):
    is_fragile: bool = Field(default=False)

class PackageTypeFePl(TypeBase, _PackageTypeCore, FePlBase):
    pass

class PackageTypeFePlUpdate(TypeUpdate):
    is_fragile: Optional[bool] = None

class PackageTypeFeRes(_PackageTypeCore, FeResBase, TypeBase):
    pass

class PackageTypeFeResLookup(FeResLookup):
    code: str
    color_code: str

class PackageTypeDb(_PackageTypeCore, DbBase, TypeBase):
    pass