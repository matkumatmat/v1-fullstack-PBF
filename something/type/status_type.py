from typing import Optional
from pydantic import Field
from ..base import (_Base, _WithDbMixin, _PublicIdentifierMixin,
                    _InternalIdentifierMixin, _TimestampMixin,
                    FeResBase, FeResLookup, FePlUpdate, FePlBase,
                    DbBase, TypeUpdate, TypeBase
)
class _StatusTypeCore(TypeBase):
    color_code: Optional[str] = Field(default=None, max_length=7)
    icon: Optional[str] = Field(default=None, max_length=50)
    css_class: Optional[str] = Field(default=None, max_length=50)
    requires_approval: bool = Field(default=False)
    sends_notification: bool = Field(default=False)

class StatusTypeFePl(TypeBase, _StatusTypeCore):
    pass

class StatusTypeFePlUpdate(TypeUpdate):
    color_code: Optional[str] = None
    icon: Optional[str] = None
    css_class: Optional[str] = None
    requires_approval: Optional[bool] = None
    sends_notification: Optional[bool] = None

class StatusTypeFeRes(_StatusTypeCore, FeResBase, TypeBase):
    pass

class StatusTypeFeResLookup(FeResLookup):
    code: str
    color_code: str
    requires_approval: bool
    css_class: str

class StatusTypeDb(_StatusTypeCore, DbBase, TypeBase):
    pass