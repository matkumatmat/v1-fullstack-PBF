# file: app/api/routers/type/document_type.py (REFAKTORED)

from app.api.utils.crud_router_factory import create_crud_router
from app.services import type_service
from app import schemas

router = create_crud_router(
    service=type_service.document_type,
    response_schema=schemas.DocumentType,
    prefix="/document-types",
    tags=["Master Data - Types"]
)