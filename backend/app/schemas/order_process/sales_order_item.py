# file: app/schemas/order_process/sales_order_item.py

import uuid
from datetime import date, datetime
from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated

from app.models.enums import SalesOrderStatusEnum
from ..type.sector_type import SectorType
from ..type.allocation_type import AllocationType
from ..type.product_price import ProductPrice

# ✅ FIXED: Use TYPE_CHECKING for circular references
if TYPE_CHECKING:
    from ..product.product import Product
    from .shipping_plan_item import ShippingPlanItem

# --- SalesOrderItem Schemas ---

class SalesOrderItemBase(BaseModel):
    """Skema dasar untuk data item SO yang disediakan pengguna."""
    product_id: int
    quantity_requested: Annotated[int, Field(..., gt=0)]
    unit_price: Decimal = Field(..., max_digits=12, decimal_places=2, gt=0)
    price_type_code_used: Annotated[str, Field(..., max_length=20)]
    line_number: Optional[int] = None
    required_delivery_date: Optional[date] = None
    product_price_id: Optional[int] = None

class SalesOrderItemCreate(SalesOrderItemBase):
    """
    Skema untuk membuat item SO baru SEBAGAI BAGIAN dari SalesOrder.
    `sales_order_id` tidak diperlukan di sini karena akan ditangani oleh relasi.
    """
    pass

class SalesOrderItemUpdate(BaseModel):
    """Skema untuk memperbarui SalesOrderItem. Semua field opsional."""
    quantity_requested: Optional[Annotated[int, Field(gt=0)]] = None
    unit_price: Optional[Decimal] = None
    price_type_code_used: Optional[Annotated[str, Field(max_length=20)]] = None
    required_delivery_date: Optional[date] = None
    status: Optional[SalesOrderStatusEnum] = None

class SalesOrderItem(SalesOrderItemBase):
    """Skema read untuk SalesOrderItem, termasuk field dari server dan relasi."""
    id: int
    public_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    status: SalesOrderStatusEnum
    total_price: Optional[Decimal]
    sales_order_id: int

    # Relasi yang di-load
    product: Optional['Product'] = None
    product_price_entry: Optional[ProductPrice] = None
    shipping_plan_items: List['ShippingPlanItem'] = []
    sectors: List[SectorType] = []
    allocations: List[AllocationType] = []

    model_config = ConfigDict(from_attributes=True)