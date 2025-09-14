import logfire
import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from logfire import ConsoleOptions, LogfireLoggingHandler

# 1. Konfigurasi Logfire untuk HANYA menggunakan output konsol.
# Ini memberitahu untuk tidak mencoba mencari token atau mengirim data ke cloud.
logfire.configure(
    send_to_logfire=False, 
    console=ConsoleOptions()
)

logfire.instrument_pydantic()

logging.basicConfig(
    level=logging.INFO,
    handlers=[LogfireLoggingHandler()],
    force=True, # force=True diperlukan untuk menimpa konfigurasi uvicorn
)

app = FastAPI(
    title="My Advanced FastAPI App",
    description="API with structured logging and observability."
)

logfire.instrument_fastapi(app)

from app.api.api import api_router

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/api")

@app.get("/")
def read_root():
    """Endpoint root sederhana untuk pengujian."""
    logfire.info('Root endpoint was called!')
    return {"message": "Welcome to the WMS API"}