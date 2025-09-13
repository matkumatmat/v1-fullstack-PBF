# file: backend/main.py (FINAL, SIMPLIFIED AND CORRECTED CODE)

import logfire
from pydantic import BaseModel
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import logging

# Impor HANYA yang diperlukan dari logfire
from logfire.integrations.logging import LogfireLoggingHandler

from app.api.api import api_router

# ===================================================================
# KONFIGURASI LOGGING DAN TRACING (SIMPLIFIED)
# ===================================================================

# 1. Konfigurasi instance Logfire global.
# Ini adalah satu-satunya tempat kita perlu berinteraksi dengan `logfire.configure`.
logfire.configure(send_to_logfire=False)

# 2. Ambil alih Logger Root Python
root_logger = logging.getLogger()

# Bersihkan handler yang sudah ada untuk menghindari duplikasi
if root_logger.hasHandlers():
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

# ===================================================================
# ❗ PERBAIKAN FINAL DI SINI ❗
# Inisialisasi LogfireLoggingHandler TANPA argumen apa pun.
# Ia dirancang untuk secara otomatis menemukan dan menggunakan
# instance Logfire yang telah dikonfigurasi secara global.
# ===================================================================
handler = LogfireLoggingHandler()
root_logger.addHandler(handler)
root_logger.setLevel(logging.INFO)

# 3. Nonaktifkan propagasi untuk logger akses Uvicorn
logging.getLogger("uvicorn.access").propagate = False
logging.getLogger("uvicorn.error").propagate = True

# 4. Instrumentasi Pydantic dan FastAPI
logfire.instrument_pydantic()
# ===================================================================

app = FastAPI(
    title="My Advanced FastAPI App",
    description="API with structured logging and observability."
)

logfire.instrument_fastapi(app)

# Daftar origin yang diizinkan. 
# Ganti dengan URL frontend Anda jika sudah di-deploy.
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Tambahkan CORSMiddleware ke aplikasi
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Izinkan semua metode (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Izinkan semua header
)

app.include_router(api_router, prefix="/api/api")