# file: app/api/routers/type/priority_level.py (REFAKTORED)

from app.api.utils.crud_router_factory import create_crud_router
from app.services import type_service
from app import schemas

router = create_crud_router(
    service=type_service.priority_level,
    response_schema=schemas.PriorityLevel,
    prefix="/priority-levels",
    tags=["Master Data - Types"]
)