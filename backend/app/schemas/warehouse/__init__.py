# file: app/schemas/warehouse/__init__.py (CLEANED UP)

from .stock_placement import StockPlacement, StockPlacementCreate, StockPlacementUpdate
from .rack import Rack, RackCreate, RackUpdate
from .warehouse import Warehouse, WarehouseCreate, WarehouseUpdate

__all__ = [
    "StockPlacement", "StockPlacementCreate", "StockPlacementUpdate",
    "Rack", "RackCreate", "RackUpdate", 
    "Warehouse", "WarehouseCreate", "WarehouseUpdate",
]

# ❌ REMOVED: Hapus redundant model_rebuild() calls
# Semua rebuilding sekarang dilakukan di schemas/__init__.py

# DEVIL'S ADVOCATE NOTE:
# File ini sekarang lebih bersih dan fokus hanya pada ekspor.
# Tidak ada lagi duplikasi model_rebuild() yang bisa menyebabkan konflik.