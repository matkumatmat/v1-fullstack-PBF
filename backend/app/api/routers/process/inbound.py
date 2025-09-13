# file: app/api/routers/process/inbound.py (FINAL & COMPLETE)

from fastapi import APIRouter, Depends, status, Query, HTTPException
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
from app.services.process import inbound as inbound_service
from app.core.exceptions import NotFoundException, BadRequestException, UnprocessableEntityException

# --- Router untuk Proses Inbound ---
router = APIRouter()

# --- ENDPOINTS PERSIAPAN FORM ---

@router.get("/inbound/form-data", response_model=InboundFormData, summary="Ambil Data Awal untuk Form Inbound")
async def get_form_data_endpoint(db: AsyncSession = Depends(get_db_session)):
    """
    Menyediakan semua data lookup (tipe, kategori, dll.) yang dibutuhkan
    oleh frontend untuk membangun form inbound.
    """
    return await inbound_service.get_inbound_form_data(db)

@router.get("/inbound/search-products", response_model=List[InboundProductSearchSchema], summary="Cari Produk untuk Inbound")
async def search_products_endpoint(
    q: str = Query(..., min_length=2, description="Teks pencarian untuk kode atau nama produk."),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Mencari produk yang ada berdasarkan kode atau nama.
    """
    return await inbound_service.search_products_for_inbound(db, query=q)

@router.get("/inbound/search-racks", response_model=List[InboundRackSearchSchema], summary="Cari Rak untuk Penempatan Stok")
async def search_racks_endpoint(
    q: str = Query(..., min_length=1, description="Teks pencarian untuk kode rak atau kode warehouse."),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Mencari rak yang tersedia (kosong) berdasarkan kodenya.
    """
    return await inbound_service.search_racks_for_inbound(db, query=q)

# --- ENDPOINT EKSEKUSI PROSES ---

@router.post("/inbound/process", response_model=InboundResponse, status_code=status.HTTP_201_CREATED, summary="Proses Inbound Lengkap")
async def process_inbound_endpoint(
    payload: InboundPayload,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Menangani seluruh alur kerja proses inbound dalam satu panggilan API atomik.
    Jika ada langkah yang gagal, seluruh proses akan dibatalkan (rollback).
    """
    try:
        result = await inbound_service.process_full_inbound(db, payload=payload)
        return result
    except (NotFoundException, BadRequestException, UnprocessableEntityException) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except Exception as e:
        # Menangkap error tak terduga lainnya
        # Sebaiknya log error ini untuk debugging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected internal error occurred: {e}"
        )