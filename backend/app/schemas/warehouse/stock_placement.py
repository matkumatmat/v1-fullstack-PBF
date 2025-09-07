# file: app/schemas/warehouse/stock_placement.py

import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated

# from ..product.allocation import Allocation # Dihindari untuk circular import
#from .rack import Rack
from typing import TYPE_CHECKING
# --- Forward Reference Rebuilding ---
from ..product.allocation import Allocation
if TYPE_CHECKING:
    from .warehouse import Warehouse
    from .rack import Rack

# --- StockPlacement Schemas ---

class StockPlacementBase(BaseModel):
    """Skema dasar untuk peristiwa penempatan stok."""
    rack_id: int
    allocation_id: int
    quantity: Annotated[int, Field(..., gt=0, description="Quantity placed must be positive.")]
    placed_by: Optional[Annotated[str, Field(max_length=50)]] = None

class StockPlacementCreate(StockPlacementBase):
    """Skema untuk membuat StockPlacement baru. Ini adalah aksi 'putaway'."""
    pass

# DEVIL'S ADVOCATE NOTE: Update untuk StockPlacement biasanya tidak umum.
# Biasanya Anda akan menghapus penempatan lama dan membuat yang baru (pergerakan stok).
# Namun, kita sediakan skema update jika diperlukan untuk koreksi.
class StockPlacementUpdate(BaseModel):
    """Skema untuk memperbarui StockPlacement. Jarang digunakan."""
    quantity: Optional[Annotated[int, Field(gt=0)]] = None
    placed_by: Optional[Annotated[str, Field(max_length=50)]] = None

class StockPlacement(StockPlacementBase):
    """Skema read untuk StockPlacement, termasuk field dari server dan relasi."""
    id: int
    public_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    placement_date: datetime

    # Relasi yang di-load
    rack: Optional['Rack'] = None
    allocation: Optional['Allocation'] = None

    model_config = ConfigDict(from_attributes=True)

