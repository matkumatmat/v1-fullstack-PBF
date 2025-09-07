# file: app/api/routers/type/packaging_material.py (REFAKTORED)

from app.api.utils.crud_router_factory import create_crud_router
from app.services import type_service
from app import schemas

router = create_crud_router(
    service=type_service.packaging_material,
    response_schema=schemas.PackagingMaterial,
    prefix="/packaging-materials",
    tags=["Master Data - Types"]
)