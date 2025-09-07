# backend/main.py

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.api import api_router

app = FastAPI()

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