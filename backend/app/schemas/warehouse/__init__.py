# file: app/schemas/warehouse/__init__.py

from .stock_placement import StockPlacement, StockPlacementCreate, StockPlacementUpdate
from .rack import Rack, RackCreate, RackUpdate
from .warehouse import Warehouse, WarehouseCreate, WarehouseUpdate

# DEVIL'S ADVOCATE NOTE:
# Ini adalah titik pusat untuk menyelesaikan semua referensi string.
# Setelah semua skema diimpor, kita panggil `model_rebuild()` pada skema
# yang memiliki referensi string ('forward references').
Warehouse.model_rebuild()
Rack.model_rebuild()
StockPlacement.model_rebuild()