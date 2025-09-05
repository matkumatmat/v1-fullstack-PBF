from fastapi import FastAPI
from app.routes.v1.api import api_router

def create_app():
    app = FastAPI()
    app.include_router(api_router, prefix="/api/v1")
    return app
