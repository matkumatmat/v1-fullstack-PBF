from typing import Optional
from decimal import Decimal
from pydantic import Field, BaseModel, ConfigDict
from datetime import date, datetime  
from ..base import (_Base, _WithDbMixin, _PublicIdentifierMixin,
                    _InternalIdentifierMixin, _TimestampMixin,
                    FeResBase, FeResLookup, FePlUpdate, FePlBase,
                    DbBase, TypeUpdate, TypeBase
)

class _DeliveryTypeCore(_Base):
    estimated_days:Optional[int]
    cost_per_kg: Optional[float]
    cost_per_km: Optional[float]
    is_active: bool = Field(default=True)

class DeliveryTypeFePl(TypeBase, _DeliveryTypeCore, FePlBase):
    pass

class DeliveryTypeFePlUpdate(TypeUpdate, _DeliveryTypeCore):
    pass

class DeliveryTypeFeRes(_DeliveryTypeCore, FeResBase, TypeBase):
    pass

class DeliveryTypeFeResLookup(FeResLookup):
    code: str
    name: str
    estimated_days: int
    cost_per_km: float

class DeliveryTypeDb(_DeliveryTypeCore, DbBase, TypeBase):
    pass