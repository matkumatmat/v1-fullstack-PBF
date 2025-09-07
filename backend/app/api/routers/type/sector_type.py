# file: app/api/routers/type/sector_type.py (REFAKTORED)

from app.api.utils.crud_router_factory import create_crud_router
from app.services import type_service
from app import schemas

router = create_crud_router(
    service=type_service.sector_type,
    response_schema=schemas.SectorType,
    prefix="/sector-types",
    tags=["Master Data - Types"]
)