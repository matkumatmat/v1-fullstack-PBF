from fastapi import FastAPI
from .api.api import api_router
from .config import settings

def create_app() -> FastAPI:
    """
    Application factory function.
    Initializes the FastAPI application and includes the main API router.
    """
    # Initialize the FastAPI app
    app = FastAPI(
        title="Warehouse Management System API",
        description="The API for the WMS application.",
        version="0.1.0"
    )

    # Include the main router
    # All routes defined in the /api/endpoints directory will be available under /api
    app.include_router(api_router, prefix="/api")

    # You can add startup/shutdown events here if needed
    # @app.on_event("startup")
    # async def startup_event():
    #     print("Application startup")

    # @app.on_event("shutdown")
    # async def shutdown_event():
    #     print("Application shutdown")

    return app
