# file: app/schemas/order_process/sales_order.py

import uuid
from datetime import date, datetime
from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated

from app.models.enums import SalesOrderStatusEnum
from .sales_order_item import SalesOrderItem, SalesOrderItemCreate # <-- Impor skema Create
if TYPE_CHECKING:
    from ..customer.customer import Customer
    from .shipping_plan import ShippingPlan
# --- SalesOrder Schemas ---

class SalesOrderBase(BaseModel):
    """Skema dasar dengan field yang dapat diinput oleh pengguna untuk SalesOrder."""
    so_number: Annotated[str, Field(..., max_length=50)]
    customer_id: int
    so_date: date
    input_by: Optional[Annotated[str, Field(max_length=50)]] = None
    notes: Optional[str] = None
    special_instructions: Optional[str] = None
    is_tender_so: bool = Field(default=False)

class SalesOrderCreate(SalesOrderBase):
    """
    Skema untuk membuat SalesOrder baru, termasuk semua itemnya dalam satu request.
    Ini memungkinkan pembuatan yang atomik dan efisien.
    """
    items: List[SalesOrderItemCreate] = Field(..., min_length=1, description="List of items in this sales order.")

class SalesOrderUpdate(BaseModel):
    """Skema untuk memperbarui SalesOrder. Biasanya terbatas pada field non-transaksional."""
    so_number: Optional[Annotated[str, Field(max_length=50)]] = None
    so_date: Optional[date] = None
    status: Optional[SalesOrderStatusEnum] = None
    input_by: Optional[Annotated[str, Field(max_length=50)]] = None
    notes: Optional[str] = None
    special_instructions: Optional[str] = None
    is_tender_so: Optional[bool] = None

class SalesOrder(SalesOrderBase):
    """Skema read untuk SalesOrder, termasuk field dari server dan relasi."""
    id: int
    public_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    status: SalesOrderStatusEnum
    total_amount: Optional[Decimal]

    # Relasi yang di-load
    customer: Optional['Customer'] = None
    items: List[SalesOrderItem] = []
    shipping_plans: List['ShippingPlan'] = []

    model_config = ConfigDict(from_attributes=True)