from typing import Optional
from pydantic import Field
from ..base import (_Base, _WithDbMixin, _PublicIdentifierMixin,
                    _InternalIdentifierMixin, _TimestampMixin,
                    FeResBase, FeResLookup, FePlUpdate, FePlBase,
                    DbBase, TypeUpdate, TypeBase
)

class _MovementTypeCore(TypeBase):
    direction:Optional[str]
    auto_generate_document:Optional[bool] = Field(default=True)
    document_prefix:Optional[str]

class MovementTypeFePl(TypeBase, _MovementTypeCore, FePlBase):
    pass

class MovementTypeFePlUpdate(TypeUpdate):
    pass

class  MovementTypeFeRes(_MovementTypeCore, FeResBase, TypeBase):
    pass

class MovementTypeFeResLookup(FeResLookup):
    pass

class MovementTypeDb(_MovementTypeCore, DbBase, TypeBase)    :
    direction:str
    auto_generate_document:bool
    document_prefix:str

