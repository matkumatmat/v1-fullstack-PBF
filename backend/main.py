# file: main.py (REVISED LOGFIRE CONFIGURATION)

import logfire
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# --- [BAGIAN 1: KONFIGURASI LOGFIRE UNTUK PENGEMBANGAN LOKAL] ---
# ✅ PERBAIKAN: Konfigurasi eksplisit untuk mode offline/konsol.

from logfire.exporters.console import ConsoleExporter
from logfire.propagate import set_propagator
from opentelemetry.propagators.noop import NoOpTextMapPropagator

# 1. Nonaktifkan propagasi otomatis (tidak relevan untuk mode konsol)
set_propagator(NoOpTextMapPropagator())

# 2. Konfigurasi Logfire untuk HANYA menggunakan ConsoleExporter.
# Ini memberitahunya untuk tidak mencoba mencari token atau mengirim data ke cloud.
logfire.configure(
    send_to_logfire=False, # Eksplisit lebih baik
    exporters=[ConsoleExporter()],
)

# 3. Lanjutkan dengan instrumentasi seperti biasa.
logfire.instrument_pydantic()
# -----------------------------------------------------------------

# --- [BAGIAN 2: INISIALISASI APLIKASI FASTAPI] ---
app = FastAPI(
    title="My Advanced FastAPI App",
    description="API with structured logging and observability."
)

# --- [BAGIAN 3: INSTRUMENTASI FASTAPI] ---
logfire.instrument_fastapi(app)
# -----------------------------------------

# --- [BAGIAN 4: KONFIGURASI APLIKASI LAINNYA] ---
from app.api.api import api_router

# ... (sisa kode CORS dan include_router Anda tetap sama) ...
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