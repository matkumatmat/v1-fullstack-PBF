from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID

from ..package_type import PackageType
from ..temperature_type import TemperatureType
from ..allocation_type import AllocationType
from ..product_type import ProductType
from ..product_price import ProductPrice
from ..customer.customer_schemas import Customer
from ..warehouse.warehouse_schemas import Rack, RackAllocation
from ..order_process.sales_order_schemas import SalesOrderItem


from pydantic import BaseModel

# Pydantic V2 Schemas for SQLAlchemy Models

# --- Product Schemas ---

class ProductBase(BaseModel):
    product_code: str
    name: str
    manufacturer: Optional[str] = None
    product_type_id: int
    package_type_id: int
    temperature_type_id: int

class ProductCreate(ProductBase):
    """
    Schema for creating a new Product.
    Does not include auto-generated fields like `id` or `public_id`.
    """
    pass

class ProductUpdate(ProductBase):
    """
    Schema for updating an existing Product.
    All fields are optional for partial updates.
    Usage: ProductUpdate(...).model_dump(exclude_unset=True)
    """
    product_code: Optional[str] = None
    name: Optional[str] = None
    manufacturer: Optional[str] = None
    product_type_id: Optional[int] = None
    package_type_id: Optional[int] = None
    temperature_type_id: Optional[int] = None

class ProductInDBBase(ProductBase):
    id: int
    public_id: UUID
    # relationships
    batches: List['Batch'] = []
    product_type: Optional['ProductType'] = None
    package_type: Optional['PackageType'] = None
    temperature_type: Optional['TemperatureType'] = None
    sales_order_items: List['SalesOrderItem'] = []
    #picking_order_items = relationship('PickingOrderItem', back_populates='product')
    prices: List['ProductPrice'] = []

    class Config:
        from_attributes = True

class Product(ProductInDBBase):
    pass

# --- Batch Schemas ---

class BatchBase(BaseModel):
    lot_number: str
    expiry_date: date
    NIE: str
    received_quantity: int
    receipt_document: str
    receipt_date: date
    receipt_pic: Optional[str] = None
    receipt_doc_url: Optional[str] = None
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    product_id: int

class BatchCreate(BatchBase):
    """
    Schema for creating a new Batch.
    Does not include auto-generated fields like `id` or `public_id`.
    """
    pass

class BatchUpdate(BatchBase):
    """
    Schema for updating an existing Batch.
    All fields are optional for partial updates.
    Usage: BatchUpdate(...).model_dump(exclude_unset=True)
    """
    lot_number: Optional[str] = None
    expiry_date: Optional[date] = None
    NIE: Optional[str] = None
    received_quantity: Optional[int] = None
    receipt_document: Optional[str] = None
    receipt_date: Optional[date] = None
    receipt_pic: Optional[str] = None
    receipt_doc_url: Optional[str] = None
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    product_id: Optional[int] = None

class BatchInDBBase(BatchBase):
    id: int
    public_id: UUID
    # relationships
    product: Optional['Product'] = None
    allocations: List['Allocation'] = []
    #stock_movements = relationship('StockMovement', back_populates='batch')

    class Config:
        from_attributes = True

class Batch(BatchInDBBase):
    pass

# --- Allocation Schemas ---

class AllocationBase(BaseModel):
    # Fields that clients can provide and do not have SQLAlchemy defaults,
    # or are nullable without a default.
    allocation_number: Optional[str] = None
    expiry_date: Optional[date] = None
    special_instructions: Optional[str] = None
    handling_requirements: Optional[str] = None
    unit_cost: Optional[Decimal] = None
    total_value: Optional[Decimal] = None
    batch_id: int
    allocation_type_id: int
    customer_id: Optional[int] = None

class AllocationCreate(AllocationBase):
    """
    Schema for creating a new Allocation.
    Does not include auto-generated fields like `id`, `public_id`,
    or fields with server-side/database-side default values
    (e.g., `allocated_quantity`, `shipped_quantity`, `status`, `allocation_date`).
    """
    pass

class AllocationUpdate(AllocationBase):
    """
    Schema for updating an existing Allocation.
    All fields are optional for partial updates, including those with database defaults.
    Usage: AllocationUpdate(...).model_dump(exclude_unset=True)
    """
    # Fields from AllocationBase
    allocation_number: Optional[str] = None
    expiry_date: Optional[date] = None
    special_instructions: Optional[str] = None
    handling_requirements: Optional[str] = None
    unit_cost: Optional[Decimal] = None
    total_value: Optional[Decimal] = None
    batch_id: Optional[int] = None
    allocation_type_id: Optional[int] = None
    customer_id: Optional[int] = None

    # Fields that have defaults in DB, but can be updated by client
    allocated_quantity: Optional[int] = None
    shipped_quantity: Optional[int] = None
    reserved_quantity: Optional[int] = None
    status: Optional[str] = None
    allocation_date: Optional[date] = None
    priority_level: Optional[int] = None
    original_reserved_quantity: Optional[int] = None
    customer_allocated_quantity: Optional[int] = None

class AllocationInDBBase(AllocationBase):
    id: int
    public_id: UUID
    # Fields with SQLAlchemy defaults, included in read schema
    allocated_quantity: int = 0
    shipped_quantity: int = 0
    reserved_quantity: int = 0
    status: str = 'active'
    allocation_date: date
    priority_level: int = 5
    original_reserved_quantity: int = 0
    customer_allocated_quantity: int = 0

    # --- Relationships ---
    batch: Optional['Batch'] = None
    allocation_type: Optional['AllocationType'] = None
    customer: Optional['Customer'] = None
    # TAMBAHAN: Relationship ke picking dan stock movement
    #picking_order_items = relationship('PickingOrderItem', back_populates='allocation')
    #picking_list_items = relationship('PickingListItem', back_populates='allocation')
    #consignments = relationship('Consignment', back_populates='allocation')
    #stock_movements = relationship('StockMovement', back_populates='allocation')
    racks: List['Rack'] = []
    rack_allocations: List['RackAllocation'] = []
    # TAMBAHAN: Contract reference untuk tender
    #tender_contract_id = Column(Integer, ForeignKey('tender_contracts.id'), nullable=True)
    #tender_contract = relationship('TenderContract', back_populates='allocations')

    class Config:
        from_attributes = True

class Allocation(AllocationInDBBase):
    pass

# --- Forward Reference Rebuilding ---
# Rebuild schemas to resolve forward references like 'Batch', 'ProductType', etc.
# Note: For models like 'ProductType', 'SalesOrderItem' etc., which are not defined
# in this script, Pydantic will treat them as any type if not explicitly
# defined later or if no explicit placeholder BaseModel is used.
# The rebuild is crucial for the schemas defined here that use these string references.
Product.model_rebuild()
Batch.model_rebuild()
Allocation.model_rebuild()