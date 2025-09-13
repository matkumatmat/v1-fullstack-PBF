# file: app/api/api.py (FINAL, CLEAN VERSION)

from fastapi import APIRouter

# --- [BAGIAN 1: IMPOR MODUL ROUTER] ---
# Impor modul-modul yang berisi definisi APIRouter Anda.
# Kita menggunakan alias (as ...) untuk memberikan nama yang pendek dan jelas.

# Impor router untuk proses bisnis
from .routers.process import inbound as router_inbound
from .routers.process import consignment as router_consignment
from .routers.process import tender as router_tender

# Impor router untuk entitas produk & inventory
from .routers.product import product as router_product
from .routers.product import allocation as router_allocation

# Impor router untuk entitas warehouse
from .routers import warehouse_routes as router_warehouse

# Impor router untuk semua Tipe (Lookup Tables)
from .routers.type import allocation_type as router_allocation_type
from .routers.type import customer_type as router_customer_type
from .routers.type import delivery_type as router_delivery_type
from .routers.type import document_type as router_document_type
from .routers.type import location_type as router_location_type
from .routers.type import movement_type as router_movement_type
from .routers.type import notification_type as router_notification_type
from .routers.type import package_type as router_package_type
from .routers.type import packaging_box_type as router_packaging_box_type
from .routers.type import packaging_material as router_packaging_material
from .routers.type import priority_level as router_priority_level
from .routers.type import product_price as router_product_price
from .routers.type import product_type as router_product_type
from .routers.type import sector_type as router_sector_type
from .routers.type import status_type as router_status_type
from .routers.type import temperature_type as router_temperature_type


# --- [BAGIAN 2: INISIALISASI ROUTER UTAMA] ---
api_router = APIRouter()


# --- [BAGIAN 3: PENYERTAAN (INCLUDE) ROUTER] ---
# Menyertakan setiap sub-router dengan prefix dan tag yang logis dan terpusat.

# 3.1: Router Proses Bisnis
api_router.include_router(router_inbound.router, prefix="/process", tags=["Business Processes"])
api_router.include_router(router_consignment.router, prefix="/process/consignment", tags=["Business Processes - Consignment"])
api_router.include_router(router_tender.router, prefix="/process/tender", tags=["Business Processes - Tender"])

# 3.2: Router Entitas Inti
api_router.include_router(router_product.router, prefix="/products", tags=["Products & Inventory"])
api_router.include_router(router_allocation.router, prefix="/allocations", tags=["Products & Inventory"])
api_router.include_router(router_warehouse.router, prefix="/warehouses", tags=["Warehouses"])

# 3.3: Router Tipe (Lookup Tables)
# Semua router tipe dikelompokkan di bawah prefix /types dan satu tag untuk kerapian.
api_router.include_router(router_allocation_type.router, prefix="/types", tags=["Configuration - Types"])
api_router.include_router(router_customer_type.router, prefix="/types", tags=["Configuration - Types"])
api_router.include_router(router_delivery_type.router, prefix="/types", tags=["Configuration - Types"])
api_router.include_router(router_document_type.router, prefix="/types", tags=["Configuration - Types"])
api_router.include_router(router_location_type.router, prefix="/types", tags=["Configuration - Types"])
api_router.include_router(router_movement_type.router, prefix="/types", tags=["Configuration - Types"])
api_router.include_router(router_notification_type.router, prefix="/types", tags=["Configuration - Types"])
api_router.include_router(router_package_type.router, prefix="/types", tags=["Configuration - Types"])
api_router.include_router(router_packaging_box_type.router, prefix="/types", tags=["Configuration - Types"])
api_router.include_router(router_packaging_material.router, prefix="/types", tags=["Configuration - Types"])
api_router.include_router(router_priority_level.router, prefix="/types", tags=["Configuration - Types"])
api_router.include_router(router_product_price.router, prefix="/types", tags=["Configuration - Types"])
api_router.include_router(router_product_type.router, prefix="/types", tags=["Configuration - Types"])
api_router.include_router(router_sector_type.router, prefix="/types", tags=["Configuration - Types"])
api_router.include_router(router_status_type.router, prefix="/types", tags=["Configuration - Types"])
api_router.include_router(router_temperature_type.router, prefix="/types", tags=["Configuration - Types"])