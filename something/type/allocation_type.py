from typing import Optional
from ..base import (_Base, _WithDbMixin, _PublicIdentifierMixin,
                    _InternalIdentifierMixin, _TimestampMixin,
                    FeResBase, FeResLookup, FePlUpdate, FePlBase,
                    DbBase, TypeUpdate, TypeBase
)

class _AllocationTypeCore(TypeBase): 
    color_code: Optional[str] = None
    icon: Optional[str] = None

class AllocationTypeFePl(TypeBase, _AllocationTypeCore, FePlBase):
    pass

class AllocationTypeFePlUpdate(TypeUpdate):
    color_code: Optional[str] = None
    icon: Optional[str] = None

class AllocationTypeFeRes(_AllocationTypeCore, FeResBase, TypeBase):
    pass

class AllocationTypeFeResLookup(FeResLookup):
    code: str
    color_code: str

class AllocationTypeDb(_AllocationTypeCore, DbBase, TypeBase):
    pass