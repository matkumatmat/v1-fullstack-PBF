from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .services.exceptions import WMSException, ValidationError, NotFoundError, ConflictError
from .api.v1.customer import customer_routes
from .api.v1.product import product_routes
from .responses import APIResponse

def create_app():
    app = FastAPI(
        title="Warehouse Management System API",
        description="API for managing warehouse operations, inventory, and logistics.",
        version="1.0.0",
    )

    # Exception Handlers
    @app.exception_handler(WMSException)
    async def wms_exception_handler(request: Request, exc: WMSException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=APIResponse.error(message=exc.message, code=exc.error_code, details=exc.details).model_dump()
        )

    @app.exception_handler(NotFoundError)
    async def not_found_error_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=APIResponse.error(message=exc.message, code=exc.error_code).model_dump()
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=APIResponse.error(message=exc.message, code=exc.error_code, details={'field': exc.field}).model_dump()
        )

    @app.exception_handler(ConflictError)
    async def conflict_error_handler(request: Request, exc: ConflictError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=APIResponse.error(message=exc.message, code=exc.error_code).model_dump()
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=APIResponse.error(
                message="Request validation failed",
                code="REQUEST_VALIDATION_ERROR",
                details=[error for error in exc.errors()]
            ).model_dump()
        )

    # Register Routers
    app.include_router(customer_routes.customer_router, prefix="/api/v1/customers", tags=["Customers"])
    app.include_router(product_routes.router, prefix="/api/v1/products", tags=["Products"])

    return app
