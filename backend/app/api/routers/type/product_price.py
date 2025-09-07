# file: app/api/routers/type/product_price.py (REFAKTORED)

from app.api.utils.crud_router_factory import create_crud_router
from app.services import type_service
from app import schemas

router = create_crud_router(
    service=type_service.product_price,
    response_schema=schemas.ProductPrice,
    prefix="/product-prices",
    tags=["Master Data - Types"]
)