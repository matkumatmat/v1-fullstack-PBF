# file: app/api/api.py

from fastapi import APIRouter

# --- Impor Router ---

# 1. Impor modul router tipe dari direktori `type`
#    Pastikan Anda memiliki `__init__.py` di `app/api/routers/` dan `app/api/routers/type/`
from app.api.routers.type import (
    allocation_type,
    customer_type,
    delivery_type,
    document_type,
    location_type,
    movement_type,
    notification_type,
    package_type,
    packaging_box_type,
    packaging_material,
    priority_level,
    product_price,
    product_type,
    sector_type,
    status_type,
    temperature_type,
)

# 2. Impor modul router entitas utama
from .routers import (
    warehouse_routes,
    process,
    product,
    #order_process,
)

from app.api.routers.process import (
    inbound, consignment, tender
)
from app.api.routers.product import (
    allocation
)

# --- Inisialisasi Router Utama ---
api_router = APIRouter()


# --- Penyertaan Router Tipe ---
# Setiap `.router` di sini adalah objek APIRouter yang dibuat oleh pabrik kita.
api_router.include_router(allocation_type.router)
api_router.include_router(customer_type.router)
api_router.include_router(delivery_type.router)
api_router.include_router(document_type.router)
api_router.include_router(location_type.router)
api_router.include_router(movement_type.router)
api_router.include_router(notification_type.router)
api_router.include_router(package_type.router)
api_router.include_router(packaging_box_type.router)
api_router.include_router(packaging_material.router)
api_router.include_router(priority_level.router)
api_router.include_router(product_price.router)
api_router.include_router(product_type.router)
api_router.include_router(sector_type.router)
api_router.include_router(status_type.router)
api_router.include_router(temperature_type.router)


# --- Penyertaan Router Entitas/Proses ---
# Router ini didefinisikan secara manual di file masing-masing.
api_router.include_router(warehouse_routes.router)
#api_router.include_router(customer.router)
api_router.include_router(product.router)
#api_router.include_router(order_process.router)
api_router.include_router(inbound.router)
api_router.include_router(consignment.router)
api_router.include_router(tender.router)
api_router.include_router(allocation.router)
