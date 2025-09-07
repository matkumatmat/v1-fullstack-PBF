# file: app/api/routers/type/location_type.py (REFAKTORED)

from app.api.utils.crud_router_factory import create_crud_router
from app.services import type_service
from app import schemas

router = create_crud_router(
    service=type_service.location_type,
    response_schema=schemas.LocationType,
    prefix="/location-types",
    tags=["Master Data - Types"]
)