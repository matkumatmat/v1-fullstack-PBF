# file: app/schemas/customer/customer.py

import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated

# Impor skema lain yang dibutuhkan
from .customer_address import CustomerAddress, CustomerAddressCreate
from ..type.customer_type import CustomerType
from ..type.sector_type import SectorType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..product.allocation import Allocation
    from ..order_process.sales_order import SalesOrder

# --- Customer Schemas ---

class CustomerBase(BaseModel):
    """Skema dasar untuk data pelanggan yang disediakan pengguna."""
    code: Annotated[str, Field(..., max_length=20)]
    name: Annotated[str, Field(..., max_length=100)]
    customer_type_id: int
    sector_type_id: int

class CustomerCreate(CustomerBase):
    """

    Skema untuk membuat pelanggan baru, dengan dukungan pembuatan alamat secara bersamaan.
    """
    addresses: List[CustomerAddressCreate] = Field(default=[], description="A list of initial addresses for the customer.")

class CustomerUpdate(BaseModel):
    """Skema untuk memperbarui data inti pelanggan."""
    code: Optional[Annotated[str, Field(max_length=20)]] = None
    name: Optional[Annotated[str, Field(max_length=100)]] = None
    customer_type_id: Optional[int] = None
    sector_type_id: Optional[int] = None

class Customer(CustomerBase):
    """Skema read untuk pelanggan, termasuk relasi."""
    id: int
    public_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    addresses: List[CustomerAddress] = []
    customer_type: Optional[CustomerType] = None
    sector_type: Optional[SectorType] = None
    allocations: List['Allocation'] = []
    sales_orders: List['SalesOrder'] = []

    model_config = ConfigDict(from_attributes=True)

# --- Forward Reference Rebuilding ---
from ..product.allocation import Allocation
from ..order_process.sales_order import SalesOrder
Customer.model_rebuild()