from __future__ import annotations
from sqlalchemy import (
    String, ForeignKey, Text, Boolean, Numeric, Enum as SQLAlchemyEnum, Integer, 
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
import enum

from ..configuration import BaseModel

class CustomerTypeEnum(str, enum.Enum)    :
    PEMERINTAH ="PEMERINTAH"
    DISTRIBUTOR = "DISTRIBUTOR"
    RETAIL = "RETAIL"

class CustomerSpecification(BaseModel):
    __tablename__ = 'customer_specifications'
    customer_id :Mapped[int]=mapped_column(ForeignKey('customers.id'), unique=True, nullable=False)
    default_credit_limit: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), default=0.0)
    current_credit_limit: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), default=0.0)
    default_payment_terms_days: Mapped[Optional[int]] = mapped_column(Integer, default=30)
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
        return[Branch for branch in self.branches if branch.parent_id is None]
    
    def __repr__(self) -> str:
        return f'<Customer name="{self.name}">'
    
class Branch(BaseModel):
    __tablename__='branches'
    name:Mapped[str]= mapped_column(String(150), nullable=False)
    customer_id: Mapped[int]= mapped_column(ForeignKey('customers.id'), nullable=False)
    parent_id:Mapped[Optional[int]]= mapped_column(ForeignKey('branches.id'), index=True)
    customer:Mapped[Customer] = relationship(back_populates='branches')
    children:Mapped[List[Branch]]= relationship(back_populates='parent', cascade='all, delete-orphan')
    parent: Mapped[Optional[Branch]]= relationship(remote_side='Branch.id', back_populates='children')
    locations: Mapped[List[Location]]=relationship(back_populates='branch', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'<Branch name="{self.name}"'
    
class Location(BaseModel):
    __tablename__='locations'
    branch_id:Mapped[int]=mapped_column(ForeignKey('branches.id'), nullable=False)
    branch: Mapped[Branch] = relationship(back_populates='locations')
    name: Mapped[str]=mapped_column(String(50), comment='KFTD Bandung')
    location_type:Mapped[str]=mapped_column(String(50), comment='GUDANG, PENERUSAN')
    country:Mapped[Optional[str]]=mapped_column(String(50))
    state_province:Mapped[Optional[str]]=mapped_column(String(50))
    postal_code:Mapped[Optional[str]]=mapped_column(String(15))
    city:Mapped[Optional[str]]=mapped_column(String(50))
    addr_line_1:Mapped[Optional[str]]=mapped_column(String(200))
    addr_line_2:Mapped[Optional[str]]=mapped_column(String(200))
    addr_line_3:Mapped[Optional[str]]=mapped_column(String(200))
    longitude: Mapped[Optional[float]] = mapped_column(Numeric(9, 6))
    latitude: Mapped[Optional[float]] = mapped_column(Numeric(9, 6))
    is_default:Mapped[bool]=mapped_column(Boolean)
    is_active:Mapped[bool]=mapped_column(Boolean)
    location_pic:Mapped[str]=mapped_column(String(20))
    location_pic_contact: Mapped[str]=mapped_column(String(15))
    minimal_order_value: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    delivery_instructions: Mapped[Optional[str]] = mapped_column(Text)    



