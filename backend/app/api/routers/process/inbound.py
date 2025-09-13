# file: app/api/routers/process/inbound.py

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# Impor dependensi, skema, dan service yang relevan
from app.api.deps import get_db_session
from app.schemas.process.inbound import (
    InboundPayload, 
    InboundResponse, 
    InboundProductSearchSchema,
    InboundFormData,
    InboundRackSearchSchema
)
from app.services.process import inbound

# --- Router untuk Proses Inbound ---
router = APIRouter(
    prefix="/inbound",
    tags=["Business Processes - Inbound"]
)

# --- ENDPOINTS PERSIAPAN FORM ---

@router.get("/form-data", response_model=InboundFormData, summary="Ambil Data Awal untuk Form Inbound")
async def get_form_data_endpoint(db: AsyncSession = Depends(get_db_session)):
    """
    Endpoint "pemicu" yang menyediakan semua data lookup (tipe, kategori, dll.)
    yang dibutuhkan oleh frontend untuk membangun form inbound.
    Panggil endpoint ini **satu kali** saat halaman inbound dimuat.
    """
    return await inbound.process_full_inbound(db)

@router.get("/search-products", response_model=List[InboundProductSearchSchema], summary="Cari Produk untuk Inbound")
async def search_products_endpoint(
    q: str = Query(..., min_length=2, description="Teks pencarian untuk kode atau nama produk."),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Endpoint ringan untuk mencari produk yang ada berdasarkan kode atau nama.
    """
    return await inbound.search_products_for_inbound(db, query=q)

@router.get("/search-racks", response_model=List[InboundRackSearchSchema], summary="Cari Rak untuk Penempatan Stok")
async def search_racks_endpoint(
    q: str = Query(..., min_length=1, description="Teks pencarian untuk kode rak atau kode warehouse."),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Endpoint ringan untuk mencari rak yang tersedia berdasarkan kodenya.
    """
    return await inbound.search_racks_for_inbound(db, query=q)

# --- ENDPOINT EKSEKUSI PROSES ---

@router.post("/process", response_model=InboundResponse, status_code=status.HTTP_201_CREATED, summary="Proses Inbound Lengkap")
async def process_inbound_endpoint(
    payload: InboundPayload,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Meng-handle seluruh alur kerja proses inbound dalam satu panggilan API atomik.
    """
    return await inbound.process_full_inbound(db, payload=payload)