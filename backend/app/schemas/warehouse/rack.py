# file: app/schemas/warehouse/rack.py (FIXED)

import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated

from app.models.enums import RackStatusEnum
from ..type.location_type import LocationType

# ✅ FIXED: Use TYPE_CHECKING for circular references
if TYPE_CHECKING:
    from .warehouse import Warehouse
    from .stock_placement import StockPlacement

# --- Rack Schemas ---

class RackBase(BaseModel):
    """Skema dasar dengan field yang dapat diinput oleh pengguna untuk Rack."""
    code: Annotated[str, Field(..., max_length=50)]
    warehouse_id: int
    location_type_id: Optional[int] = None
    capacity: int = Field(default=1, gt=0, description="Physical capacity of the rack (e.g., in pallets).")
    zone: Optional[Annotated[str, Field(max_length=10)]] = None
    row: Optional[Annotated[str, Field(max_length=10)]] = None
    level: Optional[Annotated[str, Field(max_length=10)]] = None

class RackCreate(RackBase):
    """Skema untuk membuat Rack baru. Perhatikan tidak ada `allocation_id` atau `quantity`."""
    pass

class RackUpdate(BaseModel):
    """Skema untuk memperbarui Rack. Semua field opsional."""
    code: Optional[Annotated[str, Field(max_length=50)]] = None
    warehouse_id: Optional[int] = None # Biasanya tidak diubah
    location_type_id: Optional[int] = None
    capacity: Optional[Annotated[int, Field(gt=0)]] = None
    zone: Optional[Annotated[str, Field(max_length=10)]] = None
    row: Optional[Annotated[str, Field(max_length=10)]] = None
    level: Optional[Annotated[str, Field(max_length=10)]] = None
    status: Optional[RackStatusEnum] = None

class Rack(RackBase):
    """Skema read untuk Rack, termasuk field dari server dan relasi."""
    id: int
    public_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    current_quantity: int
    status: RackStatusEnum

    # Relasi yang di-load
    location_type: Optional[LocationType] = None
    
    # ✅ FIXED: Use string annotations for forward references
    placement: Optional['StockPlacement'] = None

    model_config = ConfigDict(from_attributes=True)