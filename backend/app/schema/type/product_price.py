from typing import Optional
from decimal import Decimal
from datetime import date
from pydantic import Field
import uuid
from datetime import date
from ..base import (_Base, _WithDbMixin, _PublicIdentifierMixin,
                    _InternalIdentifierMixin, _TimestampMixin,
                    FeResBase, FeResLookup, FePlUpdate, FePlBase,
                    DbBase, TypeUpdate, TypeBase
)

class _ProductPriceCore(TypeBase):
    product_id: int
    effective_date: date
    HNA: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)
    HJP: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)
    HET: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)

class ProductPriceFePl(_ProductPriceCore, TypeBase, FePlBase):
    pass

class ProductPriceFeUpdate(TypeUpdate):
    product_id: Optional[int] = None
    effective_date: Optional[date] = None
    HNA: Optional[Decimal] = None
    HJP: Optional[Decimal] = None
    HET: Optional[Decimal] = None

class ProductPriceFeRes(_ProductPriceCore, FeResBase, TypeBase):
    pass

class ProductPriceFeResLookup(FeResLookup):
    product_id: uuid.UUID
    effective_date: date
    HNA: Decimal
    HJP: Decimal
    HET: Decimal

class ProductPriceDb(_ProductPriceCore, DbBase, TypeBase):
    pass