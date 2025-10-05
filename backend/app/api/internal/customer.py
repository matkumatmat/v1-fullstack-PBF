# file: app/api/routers/customer_router.py

import uuid
from typing import List
from fastapi import APIRouter, Depends, status, Query

from sqlalchemy.ext.asyncio import AsyncSession

# Impor dependensi untuk mendapatkan sesi DB
from app.api.deps import get_db_session

# Impor semua skema yang relevan
from app.schema.internal.user import customer as schemas

# Impor semua fungsi service yang akan kita panggil
from app.service import customer as customer_service

# =============================================================================
# INISIALISASI ROUTER
# =============================================================================

router = APIRouter(
    prefix="/customers",  # Semua endpoint di file ini akan diawali dengan /customers
    tags=["Customers & Branches"] # Grup di dokumentasi Swagger/OpenAPI
)

# =============================================================================
# ENDPOINTS UNTUK CUSTOMER (LEVEL ATAS)
# =============================================================================

@router.post(
    "/onboard",
    response_model=schemas.CustomerWithBranchesResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Onboard Customer Baru (Orkestrasi Penuh)"
)
async def onboard_new_customer_endpoint(
    payload: schemas.CustomerOnboard,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Membuat entitas Customer baru beserta seluruh hierarki Branch dan Location-nya
    dalam satu transaksi. Gunakan ini untuk onboarding customer baru yang kompleks.
    """
    new_customer = await customer_service.onboard_customer(db=db, payload=payload)
    return new_customer

@router.get(
    "",
    response_model=List[schemas.CustomerResponse],
    status_code=status.HTTP_200_OK,
    summary="Dapatkan Daftar Semua Customer"
)
async def get_all_customers_endpoint(
    skip: int = 0,
    limit: int = Query(default=100, lte=1000), # Batasi limit maks 1000
    db: AsyncSession = Depends(get_db_session)
):
    """
    Mengambil daftar semua customer dengan data dasar.
    Endpoint ini mendukung paginasi menggunakan parameter `skip` dan `limit`.
    """
    customers = await customer_service.get_all_customers(db=db, skip=skip, limit=limit)
    return customers

@router.get(
    "/{customer_public_id}",
    response_model=schemas.CustomerWithBranchesResponse,
    status_code=status.HTTP_200_OK,
    summary="Dapatkan Detail Lengkap Customer"
)
async def get_customer_details_endpoint(
    customer_public_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Mengambil detail lengkap seorang customer, termasuk detail finansial,
    spesifikasi, dan seluruh hierarki branch beserta lokasinya.
    """
    db_customer = await customer_service.get_customer_with_full_hierarchy(
        db=db, 
        customer_public_id=customer_public_id
    )
    return db_customer

# =============================================================================
# ENDPOINTS UNTUK BRANCH (SUB-RESOURCE DARI CUSTOMER)
# =============================================================================

@router.post(
    "/{customer_public_id}/branches",
    response_model=schemas.CustomerWithBranchesResponse, # Kembalikan customer utuh biar frontend bisa update
    status_code=status.HTTP_201_CREATED,
    summary="Tambahkan Hierarki Branch Baru ke Customer"
)
async def add_branch_to_customer_endpoint(
    customer_public_id: uuid.UUID,
    payload: schemas.BranchCreateForExistingCustomer,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Menambahkan satu atau lebih branch (beserta lokasinya) ke customer yang sudah ada.
    Payload berisi seluruh struktur hierarki branch baru yang akan ditambahkan.
    """
    updated_customer = await customer_service.add_branch_to_customer(
        db=db,
        customer_public_id=customer_public_id,
        payload=payload
    )
    return updated_customer

@router.get(
    "/branches/{branch_public_id}", # Note: prefix /customers ditambahkan otomatis
    response_model=schemas.BranchResponse,
    status_code=status.HTTP_200_OK,
    summary="Dapatkan Detail Branch"
)
async def get_branch_details_endpoint(
    branch_public_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Mengambil detail satu branch spesifik, termasuk daftar lokasinya
    dan anak-anaknya (satu level).
    """
    branch = await customer_service.get_branch_with_locations(db=db, branch_public_id=branch_public_id)
    return branch

# =============================================================================
# ENDPOINTS UNTUK LOCATION (SUB-RESOURCE DARI BRANCH)
# =============================================================================

@router.post(
    "/branches/{branch_public_id}/locations",
    response_model=schemas.LocationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tambahkan Lokasi Baru ke Branch"
)
async def add_location_to_branch_endpoint(
    branch_public_id: uuid.UUID,
    payload: schemas.LocationCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Menambahkan satu lokasi fisik baru (gudang, panel, dll.) ke branch yang sudah ada.
    """
    new_location = await customer_service.add_location_to_branch(
        db=db,
        branch_public_id=branch_public_id,
        payload=payload
    )
    return new_location

@router.post(
    "/branches/{branch_public_id}/locations",
    response_model=schemas.LocationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tambahkan Lokasi Baru ke Branch"
)
async def add_location_to_branch_endpoint(
    branch_public_id: uuid.UUID,
    payload: schemas.LocationCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Menambahkan satu lokasi fisik baru (gudang, panel, dll.) ke branch yang sudah ada.
    """
    new_location = await customer_service.add_location_to_branch(
        db=db,
        branch_public_id=branch_public_id,
        payload=payload
    )
    return new_location

@router.get(
    "/locations/{location_public_id}",
    response_model=schemas.LocationResponse,
    status_code=status.HTTP_200_OK,
    summary="Dapatkan Detail Location"
)
async def get_location_details_endpoint(
    location_public_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Mengambil detail dari satu lokasi fisik spesifik.
    """
    location = await customer_service.get_location_details(
        db=db,
        location_public_id=location_public_id
    )
    return location

@router.get(
    "/lookup/all",
    response_model=List[schemas.CustomerLookup],
    status_code=status.HTTP_200_OK,
    summary="Dapatkan Semua Customer & Hierarkinya untuk Dropdown"
)
async def get_all_customers_for_lookup_endpoint(
    db: AsyncSession = Depends(get_db_session)
):
    """
    Mengembalikan daftar SEMUA customer, branch, dan location dalam format
    nested yang ringan (hanya public_id dan name).
    
    Sangat dioptimalkan untuk mengisi data filter/dropdown di frontend.
    """
    customers = await customer_service.get_all_customers_for_lookup(db=db)
    return customers
    