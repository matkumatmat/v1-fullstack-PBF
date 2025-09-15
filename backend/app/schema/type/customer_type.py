from typing import Optional
from decimal import Decimal
from pydantic import Field
from ..base import (_Base, _WithDbMixin, _PublicIdentifierMixin,
                    _InternalIdentifierMixin, _TimestampMixin,
                    FeResBase, FeResLookup, FePlUpdate, FePlBase,
                    DbBase, TypeUpdate, TypeBase
)

class _CustomerTypeCore(_Base):
    is_active: bool = Field(default=True)
    allows_tender_allocation: bool = Field(default=False)
    requires_pre_approval: bool = Field(default=False)
    default_credit_limit: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)
    default_payment_terms_days: Optional[int] = Field(default=30)

class CustomerTypeFePl(TypeBase,_CustomerTypeCore, FePlBase):
    pass

class CustomerTypeFePlUpdate(TypeUpdate):
    is_active: bool = Field(default=True)
    allows_tender_allocation: bool = Field(default=False)
    requires_pre_approval: bool = Field(default=False)
    default_credit_limit: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)
    default_payment_terms_days: Optional[int] = Field(default=30)    

class CustomerTypeFeRes(_CustomerTypeCore, FeResBase, TypeBase):
    pass

class CustomerTypeFeResLookup(FeResLookup):
    code : str
    name : str

class CustomerTypeDb(_CustomerTypeCore, DbBase, TypeBase):
    pass
    