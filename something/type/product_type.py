# file: app/schemas/type/product_type.py

from typing import Optional
from pydantic import Field
from ..base import (_Base, _WithDbMixin, _PublicIdentifierMixin,
                    _InternalIdentifierMixin, _TimestampMixin,
                    FeResBase, FeResLookup, FePlUpdate, FePlBase,
                    DbBase, TypeUpdate, TypeBase
)

class _ProductTypeCore(TypeBase): 
    sort_order: Optional[int]

class ProductTypeFeResLookup(FeResLookup):
    pass

class ProductTypeDb(_ProductTypeCore, DbBase, TypeBase):
    pass