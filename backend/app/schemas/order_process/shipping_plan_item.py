# file: app/schemas/order_process/shipping_plan_item.py

import uuid
from datetime import date, datetime
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated

from app.models.enums import ShippingPlanStatusEnum
if TYPE_CHECKING:
    from .sales_order_item import SalesOrderItem

# --- ShippingPlanItem Schemas ---

class ShippingPlanItemBase(BaseModel):
    """Skema dasar untuk data item shipping plan yang disediakan pengguna."""
    sales_order_item_id: int
    quantity_to_fulfill: Annotated[int, Field(..., gt=0)]
    line_number: Optional[int] = None
    planned_date: Optional[date] = None

class ShippingPlanItemCreate(ShippingPlanItemBase):
    """
    Skema untuk membuat item shipping plan SEBAGAI BAGIAN dari ShippingPlan baru.
    `shipping_plan_id` tidak diperlukan di sini.
    """
    pass

class ShippingPlanItemUpdate(BaseModel):
    """Skema untuk memperbarui ShippingPlanItem. Semua field opsional."""
    quantity_to_fulfill: Optional[Annotated[int, Field(gt=0)]] = None
    line_number: Optional[int] = None
    planned_date: Optional[date] = None
    status: Optional[ShippingPlanStatusEnum] = None

class ShippingPlanItem(ShippingPlanItemBase):
    """Skema read untuk ShippingPlanItem, termasuk field dari server dan relasi."""
    id: int
    public_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    status: ShippingPlanStatusEnum
    shipping_plan_id: int

    # Relasi yang di-load
    sales_order_item: Optional['SalesOrderItem'] = None

    model_config = ConfigDict(from_attributes=True)