from fastapi import APIRouter
from . import (
    product_type,
    package_type,
    temperature_type,
    allocation_type,
    sector_type,
    customer_type,
    document_type,
    status_type,
    location_type,
    packaging_material,
    packaging_box_type,
    priority_level,
    notification_type,
    delivery_type,
    product_price,
    movement_type,
    warehouse_routes,     
)

api_router = APIRouter()

api_router.include_router(product_type.router, prefix="/product_types", tags=["product_types"])
api_router.include_router(package_type.router, prefix="/package_types", tags=["package_types"])
api_router.include_router(temperature_type.router, prefix="/temperature_types", tags=["temperature_types"])
api_router.include_router(allocation_type.router, prefix="/allocation_types", tags=["allocation_types"])
api_router.include_router(sector_type.router, prefix="/sector_types", tags=["sector_types"])
api_router.include_router(customer_type.router, prefix="/customer_types", tags=["customer_types"])
api_router.include_router(document_type.router, prefix="/document_types", tags=["document_types"])
api_router.include_router(status_type.router, prefix="/status_types", tags=["status_types"])
api_router.include_router(location_type.router, prefix="/location_types", tags=["location_types"])
api_router.include_router(packaging_material.router, prefix="/packaging_materials", tags=["packaging_materials"])
api_router.include_router(packaging_box_type.router, prefix="/packaging_box_types", tags=["packaging_box_types"])
api_router.include_router(priority_level.router, prefix="/priority_levels", tags=["priority_levels"])
api_router.include_router(notification_type.router, prefix="/notification_types", tags=["notification_types"])
api_router.include_router(delivery_type.router, prefix="/delivery_types", tags=["delivery_types"])
api_router.include_router(product_price.router, prefix="/product_prices", tags=["product_prices"])
api_router.include_router(movement_type.router, prefix="/movement_types", tags=["movement_types"])
api_router.include_router(warehouse_routes.router_warehouses, prefix="/warehouses", tags=["Warehouses"])
api_router.include_router(warehouse_routes.router_racks, prefix="/racks", tags=["Racks"])
api_router.include_router(warehouse_routes.router_rack_allocations, prefix="/rack_allocations", tags=["Rack Allocations"])
