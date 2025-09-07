# file: app/api/routers/type/delivery_type.py (REFAKTORED)

from app.api.utils.crud_router_factory import create_crud_router
from app.services import type_service
from app import schemas

# Mengikuti pola yang sama persis, hanya mengubah konteks.
router = create_crud_router(
    service=type_service.delivery_type,
    response_schema=schemas.DeliveryType,
    prefix="/delivery-types",
    tags=["Master Data - Types"]
)