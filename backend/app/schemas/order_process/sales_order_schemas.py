# Imports
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any
from datetime import date, datetime
from uuid import UUID
from decimal import Decimal

from .shipping_plan_schemas import ShippingPlan, ShippingPlanItem
# Placeholder models for relationships not defined in the provided SQLAlchemy snippets.
# These are minimal definitions to allow forward references to resolve.
# They are not subject to the full schema generation rules as they are not part of the input.
class CustomerBase(BaseModel):
    pass

class Customer(CustomerBase):
    id: int
    class Config(ConfigDict):
        from_attributes = True

class ProductBase(BaseModel):
    pass

class Product(ProductBase):
    id: int
    class Config(ConfigDict):
        from_attributes = True

class ProductPriceBase(BaseModel):
    pass

class ProductPrice(ProductPriceBase):
    id: int
    class Config(ConfigDict):
        from_attributes = True

class SectorTypeBase(BaseModel):
    pass

class SectorType(SectorTypeBase):
    id: int
    class Config(ConfigDict):
        from_attributes = True

class AllocationTypeBase(BaseModel):
    pass

class AllocationType(AllocationTypeBase):
    id: int
    class Config(ConfigDict):
        from_attributes = True

# ----------------------------------------------------------------------------------
# SalesOrder Schemas
# ----------------------------------------------------------------------------------
class SalesOrderBase(BaseModel):
    so_number: str
    customer_id: int
    so_date: date
    total_amount: Optional[Decimal] = None
    status: str # default='PENDING', nullable=False
    input_by: Optional[str] = None
    notes: Optional[str] = None
    special_instructions: Optional[str] = None
    is_tender_so: bool # default=False

class SalesOrderCreate(SalesOrderBase):
    # Used for creating new records. It must not include fields that have a server-side
    # or database-side default value (e.g., public_id, status, is_tender_so).
    so_number: str
    customer_id: int
    so_date: date
    total_amount: Optional[Decimal] = None
    input_by: Optional[str] = None
    notes: Optional[str] = None
    special_instructions: Optional[str] = None

class SalesOrderUpdate(SalesOrderBase):
    """
    Schema for partial updates of a SalesOrder record.
    All fields are optional, allowing for flexible updates.
    Use `model_dump(exclude_unset=True)` when converting to a dictionary for partial updates.
    """
    so_number: Optional[str] = None
    customer_id: Optional[int] = None
    so_date: Optional[date] = None
    total_amount: Optional[Decimal] = None
    status: Optional[str] = None
    input_by: Optional[str] = None
    notes: Optional[str] = None
    special_instructions: Optional[str] = None
    is_tender_so: Optional[bool] = None

class SalesOrderInDBBase(SalesOrderBase):
    # This schema includes all database-generated fields and relationship fields.
    id: int # Primary key, assumed to be auto-generated
    public_id: UUID # default=lambda: str(uuid.uuid4()), unique=True, nullable=False, index=True
    customer: 'Customer' # relationship('Customer', back_populates='sales_orders')
    items: List['SalesOrderItem'] = [] # relationship('SalesOrderItem', back_populates='sales_order', cascade='all, delete-orphan')
    shipping_plan: List['ShippingPlan'] = [] # relationship('ShippingPlan', back_populates='sales_order')
    #tender_contract_id = Column(Integer, ForeignKey('tender_contracts.id'), nullable=True)
    #tender_contract = relationship('TenderContract', back_populates='sales_order')
    #packing_orders = relationship('PackingOrder', back_populates='sales_order')

    class Config(ConfigDict):
        from_attributes = True

class SalesOrder(SalesOrderInDBBase):
    pass

# ----------------------------------------------------------------------------------
# SalesOrderItem Schemas
# ----------------------------------------------------------------------------------
class SalesOrderItemBase(BaseModel):
    line_number: Optional[int] = None
    quantity_requested: int
    unit_price: Decimal
    total_price: Optional[Decimal] = None
    product_id: int
    sales_order_id: int
    required_delivery_date: Optional[date] = None
    status: str # default='PENDING'
    price_type_code_used: str
    product_price_id: Optional[int] = None

class SalesOrderItemCreate(SalesOrderItemBase):
    # Used for creating new records. It must not include fields that have a server-side
    # or database-side default value (e.g., status).
    line_number: Optional[int] = None
    quantity_requested: int
    unit_price: Decimal
    total_price: Optional[Decimal] = None
    product_id: int
    sales_order_id: int
    required_delivery_date: Optional[date] = None
    price_type_code_used: str
    product_price_id: Optional[int] = None

class SalesOrderItemUpdate(SalesOrderItemBase):
    """
    Schema for partial updates of a SalesOrderItem record.
    All fields are optional, allowing for flexible updates.
    Use `model_dump(exclude_unset=True)` when converting to a dictionary for partial updates.
    """
    line_number: Optional[int] = None
    quantity_requested: Optional[int] = None
    unit_price: Optional[Decimal] = None
    total_price: Optional[Decimal] = None
    product_id: Optional[int] = None
    sales_order_id: Optional[int] = None
    required_delivery_date: Optional[date] = None
    status: Optional[str] = None
    price_type_code_used: Optional[str] = None
    product_price_id: Optional[int] = None

class SalesOrderItemInDBBase(SalesOrderItemBase):
    # This schema includes all database-generated fields and relationship fields.
    id: int # Primary key, assumed to be auto-generated
    product: 'Product' # relationship('Product', back_populates='sales_order_items')
    sales_order: 'SalesOrder' # relationship('SalesOrder', back_populates='items')
    product_price_entry: Optional['ProductPrice'] = None # relationship('ProductPrice', back_populates='sales_order_items')
    shipping_plan_items: List['ShippingPlanItem'] = [] # relationship('ShippingPlanItem', back_populates='sales_order_item', cascade='all, delete-orphan')
    sectors: List['SectorType'] = [] # relationship('SectorType', secondary=sales_order_item_sector_association, back_populates='sales_order_items')
    allocations: List['AllocationType'] = [] # relationship('AllocationType', secondary=sales_order_item_allocation_association, back_populates='sales_order_items')

    class Config(ConfigDict):
        from_attributes = True

class SalesOrderItem(SalesOrderItemInDBBase):
    pass


SalesOrderInDBBase.model_rebuild()
SalesOrder.model_rebuild()
SalesOrderItemInDBBase.model_rebuild()
SalesOrderItem.model_rebuild()
