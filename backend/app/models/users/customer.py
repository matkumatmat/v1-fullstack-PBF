from sqlalchemy import (
    String, ForeignKey, Text, Boolean, Numeric, Enum as SQLAlchemyEnum
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from ..configuration import BaseModel,AddressTypeEnum
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..configuration import CustomerType, SectorType
    from ..order_process import SalesOrder
    from ..product import Allocation

class Customer(BaseModel):
    __tablename__ = 'customers'
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    customer_type_id: Mapped[int] = mapped_column(ForeignKey('customer_types.id'), nullable=False)
    sector_type_id: Mapped[int] = mapped_column(ForeignKey('sector_types.id'), nullable=False)
    customer_type: Mapped['CustomerType'] = relationship(back_populates='customers')
    sector_type: Mapped['SectorType'] = relationship(back_populates='customers')
    sales_orders: Mapped[List['SalesOrder']] = relationship(back_populates='customer')
    allocations: Mapped[List['Allocation']] = relationship(back_populates='customer')
    #consignment_agreements: Mapped[List['ConsignmentAgreement']] = relationship(back_populates='customer')
    #consignment_statements: Mapped[List['ConsignmentStatement']] = relationship(back_populates='customer')    
    addresses: Mapped[List['CustomerAddress']] = relationship(back_populates='customer', cascade='all, delete-orphan')
    @property
    def default_address(self) -> Optional['CustomerAddress']:
        return next((addr for addr in self.addresses if addr.is_default), None)
    @property
    def delivery_addresses(self) -> List['CustomerAddress']:
        return [addr for addr in self.addresses if addr.address_type == AddressTypeEnum.DELIVERY and addr.is_active]    
    def __repr__(self) -> str:
        return f'<Customer id={self.id} tipe customer{self.customer_type.name}>'

class CustomerAddress(BaseModel):
    __tablename__ = 'customer_addresses'
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=False)
    address_name: Mapped[str] = mapped_column(String(100), nullable=False)
    address_type: Mapped[AddressTypeEnum] = mapped_column(SQLAlchemyEnum(AddressTypeEnum, name="address_type_enum", create_type=False), default=AddressTypeEnum.DELIVERY)
    address_line1: Mapped[str] = mapped_column(String(200), nullable=False)
    address_line2: Mapped[Optional[str]] = mapped_column(String(200))
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    state_province: Mapped[Optional[str]] = mapped_column(String(50))
    postal_code: Mapped[Optional[str]] = mapped_column(String(10))
    country: Mapped[str] = mapped_column(String(50), default='Indonesia')
    contact_person: Mapped[Optional[str]] = mapped_column(String(100))
    contact_phone: Mapped[Optional[str]] = mapped_column(String(20))
    contact_email: Mapped[Optional[str]] = mapped_column(String(100))
    delivery_instructions: Mapped[Optional[str]] = mapped_column(Text)
    special_requirements: Mapped[Optional[str]] = mapped_column(Text)
    latitude: Mapped[Optional[float]] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Optional[float]] = mapped_column(Numeric(9, 6))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_by: Mapped[Optional[str]] = mapped_column(String(50))
    customer: Mapped['Customer'] = relationship(back_populates='addresses')
    def __repr__(self) -> str:
        return f'<CustomerAddress id={self.id} customer_id={self.customer_id} name="{self.address_name}">'