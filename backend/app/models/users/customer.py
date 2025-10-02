from __future__ import annotations
from sqlalchemy import (
    String, ForeignKey, Text, Boolean, Numeric, Enum as SQLAlchemyEnum, Integer
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

from ..configuration import BaseModel
from ..configuration.enums import CustomerTypeEnum

class CustomerSpecification(BaseModel):
    __tablename__ = 'customer_specification'
    customer_id :Mapped[int]=mapped_column(ForeignKey('customers.id'), unique=True, nullable=False)
    default_credit_limit: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), default=0.0)
    current_credit_limit: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    default_payment_terms_days: Mapped[Optional[int]] = mapped_column(Integer, default=30)
    minimal_order_value: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    delivery_instructions: Mapped[Optional[str]] = mapped_column(Text)
    customer:Mapped[Customer]=relationship(back_populates='specification')

class CustomerDetails(BaseModel):
    __tablename__ = 'customer_details'
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), unique=True, nullable=False)
    bank: Mapped[Optional[str]] = mapped_column(String(100))
    npwp: Mapped[Optional[str]] = mapped_column(String(25), unique=True, index=True)
    rekening: Mapped[Optional[str]] = mapped_column(String(50))
    customer: Mapped[Customer] = relationship(back_populates='details')  

class Customer(BaseModel):
    __tablename__='customers'
    name : Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    customer_type: Mapped[CustomerTypeEnum]= mapped_column(
        SQLAlchemyEnum(CustomerTypeEnum, name='customer_type_enum', create_type=False),
        nullable=False
    )
    specification: Mapped[CustomerSpecification]=relationship(
        back_populates='customer', cascade='all, delete-orphan', uselist=False
    )
    details: Mapped[CustomerDetails]=relationship(
        back_populates='customer', cascade='all, delete-orphan', uselist=False
    )
    branches: Mapped[List[Branch]] = relationship(
        back_populates='customer',
        cascade='all, delete-orphan',
    )

    @property 
    def root_branches(self) -> List[Branch]:
        return[Branch for branch in self.branches if branch.parent_id is none]
    
    def __repr__(self) -> str:
        return f'<Customer name="{self.name}">'
    
class Branch(BaseModel):
    __tablename__:'Branches'
    name:Mapped[str]= mapped_column(string(150), nullable=False)

