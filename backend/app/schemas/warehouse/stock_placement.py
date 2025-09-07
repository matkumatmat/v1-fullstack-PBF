# file: app/schemas/warehouse/stock_placement.py

import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated

# DEVIL'S ADVOCATE NOTE:
# Impor tipe untuk type hinting (seperti Allocation, Rack, Warehouse)
# harus ditempatkan di dalam blok `if TYPE_CHECKING:`.
# Ini membuat tipe tersedia untuk alat analisis statis (seperti mypy)
# tetapi tidak dijalankan saat runtime, sehingga menghindari circular imports.
# Resolusi forward reference ('Allocation') akan ditangani oleh __init__.py.
if TYPE_CHECKING:
    from .rack import Rack
    from ..product.allocation import Allocation

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

