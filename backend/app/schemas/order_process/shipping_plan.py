# file: app/schemas/order_process/shipping_plan.py

import uuid
from datetime import date, datetime
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated

from app.models.enums import ShippingPlanStatusEnum
from .shipping_plan_item import ShippingPlanItem, ShippingPlanItemCreate # <-- Impor skema Create

if TYPE_CHECKING:
    from .sales_order import SalesOrder
# --- ShippingPlan Schemas ---

class ShippingPlanBase(BaseModel):
    """Skema dasar dengan field yang dapat diinput oleh pengguna untuk ShippingPlan."""
    plan_number: Annotated[str, Field(..., max_length=50)]
    sales_order_id: int
    planned_delivery_date: date
    shipping_method: Optional[Annotated[str, Field(max_length=50)]] = None
    created_by: Optional[Annotated[str, Field(max_length=50)]] = None
    delivery_address: Optional[str] = None
    contact_person: Optional[Annotated[str, Field(max_length=100)]] = None
    contact_phone: Optional[Annotated[str, Field(max_length=20)]] = None

class ShippingPlanCreate(ShippingPlanBase):
    """

    Skema untuk membuat ShippingPlan baru, termasuk semua itemnya dalam satu request.
    """
    items: List[ShippingPlanItemCreate] = Field(..., min_length=1, description="List of items to be fulfilled in this plan.")

class ShippingPlanUpdate(BaseModel):
    """Skema untuk memperbarui ShippingPlan. Semua field opsional."""
    plan_number: Optional[Annotated[str, Field(max_length=50)]] = None
    planned_delivery_date: Optional[date] = None
    actual_delivery_date: Optional[date] = None
    shipping_method: Optional[Annotated[str, Field(max_length=50)]] = None
    status: Optional[ShippingPlanStatusEnum] = None
    confirmed_by: Optional[Annotated[str, Field(max_length=50)]] = None
    delivery_address: Optional[str] = None
    contact_person: Optional[Annotated[str, Field(max_length=100)]] = None
    contact_phone: Optional[Annotated[str, Field(max_length=20)]] = None

class ShippingPlan(ShippingPlanBase):
    """Skema read untuk ShippingPlan, termasuk field dari server dan relasi."""
    id: int
    public_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    status: ShippingPlanStatusEnum
    actual_delivery_date: Optional[date] = None
    confirmed_by: Optional[Annotated[str, Field(max_length=50)]] = None
    confirmed_date: Optional[datetime] = None

    # Relasi yang di-load
    sales_order: Optional['SalesOrder'] = None
    items: List[ShippingPlanItem] = []

    model_config = ConfigDict(from_attributes=True)

