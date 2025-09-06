# Imports
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any
from datetime import date, datetime
from uuid import UUID
from decimal import Decimal

from .sales_order_schemas import SalesOrder, SalesOrderItem 
# ----------------------------------------------------------------------------------
# ShippingPlan Schemas
# ----------------------------------------------------------------------------------
class ShippingPlanBase(BaseModel):
    plan_number: str
    planned_delivery_date: date
    actual_delivery_date: Optional[date] = None
    sales_order_id: int
    shipping_method: Optional[str] = None
    status: str # default='PENDING', nullable=False
    created_by: Optional[str] = None # Tim penjualan yang buat plan
    confirmed_by: Optional[str] = None
    delivery_address: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None

class ShippingPlanCreate(ShippingPlanBase):
    # Used for creating new records. It must not include fields that have a server-side
    # or database-side default value (e.g., public_id, status, created_date).
    plan_number: str
    planned_delivery_date: date
    actual_delivery_date: Optional[date] = None
    sales_order_id: int
    shipping_method: Optional[str] = None
    created_by: Optional[str] = None
    confirmed_by: Optional[str] = None
    delivery_address: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None

class ShippingPlanUpdate(ShippingPlanBase):
    """
    Schema for partial updates of a ShippingPlan record.
    All fields are optional, allowing for flexible updates.
    Use `model_dump(exclude_unset=True)` when converting to a dictionary for partial updates.
    """
    plan_number: Optional[str] = None
    planned_delivery_date: Optional[date] = None
    actual_delivery_date: Optional[date] = None
    sales_order_id: Optional[int] = None
    shipping_method: Optional[str] = None
    status: Optional[str] = None
    created_by: Optional[str] = None
    confirmed_by: Optional[str] = None
    delivery_address: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None

class ShippingPlanInDBBase(ShippingPlanBase):
    # This schema includes all database-generated fields and relationship fields.
    id: int # Primary key, assumed to be auto-generated
    public_id: UUID # default=lambda: str(uuid.uuid4()), unique=True, nullable=False, index=True
    created_date: datetime # default=func.current_timestamp()
    confirmed_date: Optional[datetime] = None
    sales_order: 'SalesOrder' # relationship('SalesOrder', back_populates='shipping_plan')
    items: List['ShippingPlanItem'] = [] # relationship('ShippingPlanItem', back_populates='shipping_plan', cascade='all, delete-orphan')
    #picking_lists = relationship('PickingList', back_populates='shipping_plan')
    #shipment = relationship('Shipment', back_populates='shipping_plan', uselist=False)

    class Config(ConfigDict):
        from_attributes = True

class ShippingPlan(ShippingPlanInDBBase):
    pass

# ----------------------------------------------------------------------------------
# ShippingPlanItem Schemas
# ----------------------------------------------------------------------------------
class ShippingPlanItemBase(BaseModel):
    quantity_to_fulfill: int
    shipping_plan_id: int
    sales_order_item_id: int
    line_number: Optional[int] = None
    planned_date: Optional[date] = None
    status: str # default='PENDING'

class ShippingPlanItemCreate(ShippingPlanItemBase):
    # Used for creating new records. It must not include fields that have a server-side
    # or database-side default value (e.g., status).
    quantity_to_fulfill: int
    shipping_plan_id: int
    sales_order_item_id: int
    line_number: Optional[int] = None
    planned_date: Optional[date] = None

class ShippingPlanItemUpdate(ShippingPlanItemBase):
    """
    Schema for partial updates of a ShippingPlanItem record.
    All fields are optional, allowing for flexible updates.
    Use `model_dump(exclude_unset=True)` when converting to a dictionary for partial updates.
    """
    quantity_to_fulfill: Optional[int] = None
    shipping_plan_id: Optional[int] = None
    sales_order_item_id: Optional[int] = None
    line_number: Optional[int] = None
    planned_date: Optional[date] = None
    status: Optional[str] = None

class ShippingPlanItemInDBBase(ShippingPlanItemBase):
    # This schema includes all database-generated fields and relationship fields.
    id: int # Primary key, assumed to be auto-generated
    shipping_plan: 'ShippingPlan' # relationship('ShippingPlan', back_populates='items')
    sales_order_item: 'SalesOrderItem' # relationship('SalesOrderItem', back_populates='shipping_plan_items')

    class Config(ConfigDict):
        from_attributes = True

class ShippingPlanItem(ShippingPlanItemInDBBase):
    pass

# ----------------------------------------------------------------------------------
# Forward reference resolution for circular dependencies
# ----------------------------------------------------------------------------------

ShippingPlanInDBBase.model_rebuild()
ShippingPlan.model_rebuild()
ShippingPlanItemInDBBase.model_rebuild()
ShippingPlanItem.model_rebuild()