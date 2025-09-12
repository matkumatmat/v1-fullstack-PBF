# file: app/api/routers/product.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# --- Impor Dependensi, Skema, dan Service ---
# Mengimpor dependensi untuk sesi database.
from app.api.deps import get_db_session
# Mengimpor semua skema yang relevan untuk request body dan response model.
from app import schemas
# Mengimpor service layer yang berisi semua logika bisnis.
from app.services import product_service

# --- Inisialisasi Router ---
# Menggunakan satu router untuk semua entitas yang terkait erat dengan produk
# (Product, Batch, Allocation) untuk menjaga organisasi berdasarkan domain bisnis.
router = APIRouter(
    prefix="/products",  # Menambahkan prefix untuk semua endpoint di router ini
    tags=["Products & Inventory"] # Mengelompokkan semua endpoint ini di bawah satu tag di dokumentasi API
)

# ===================================================================
# 1. PRODUCT MASTER ENDPOINTS
# ===================================================================

@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
async def create_product_endpoint(
    product_data: schemas.ProductCreate, 
    db: AsyncSession = Depends(get_db_session)
):
    """
    Membuat master data produk baru.
    
    Endpoint ini memerlukan ID dari tipe-tipe yang sudah ada (ProductType, 
    PackageType, TemperatureType) untuk berhasil.
    """
    # Mendelegasikan seluruh logika pembuatan ke service layer.
    return await product_service.create_product(db=db, product_in=product_data)

@router.get("/", response_model=List[schemas.Product])
async def get_all_products_endpoint(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db_session)
):
    """
    Mengambil daftar semua master data produk dengan paginasi.
    """
    return await product_service.get_all_products(db=db, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=schemas.Product)
async def get_product_by_id_endpoint(
    product_id: int, 
    db: AsyncSession = Depends(get_db_session)
):
    """
    Mengambil detail satu produk berdasarkan ID-nya.
    """
    db_product = await product_service.get_product_by_id(db=db, product_id=product_id)
    # Penanganan eksplisit untuk kasus 'not found' di layer router.
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=schemas.Product)
async def update_product_endpoint(
    product_id: int, 
    product_data: schemas.ProductUpdate, 
    db: AsyncSession = Depends(get_db_session)
):
    """
    Memperbarui detail master data produk yang ada.
    """
    # Service `update_product` sudah menangani kasus "not found", jadi kita bisa memanggilnya langsung.
    return await product_service.update_product(db=db, product_id=product_id, product_in=product_data)

@router.delete("/{product_id}", response_model=schemas.Product)
async def delete_product_endpoint(
    product_id: int, 
    db: AsyncSession = Depends(get_db_session)
):
    """
    Menghapus master data produk.
    Akan gagal jika produk sudah memiliki batch terkait (aturan bisnis di service).
    """
    # Service `delete_product` sudah menangani kasus "not found" dan validasi bisnis.
    return await product_service.delete_product(db=db, product_id=product_id)


# ===================================================================
# 2. BATCH ENDPOINTS
# ===================================================================

@router.post("/batches/", response_model=schemas.Batch, status_code=status.HTTP_201_CREATED)
async def create_batch_endpoint(
    batch_data: schemas.BatchCreate, 
    db: AsyncSession = Depends(get_db_session)
):
    """
    Mencatat penerimaan batch baru untuk sebuah produk (proses inbound).
    """
    return await product_service.create_batch(db=db, batch_in=batch_data)

@router.get("/batches/", response_model=List[schemas.Batch])
async def get_all_batches_endpoint(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db_session)
):
    """
    Mengambil daftar semua batch yang tercatat di sistem.
    """
    return await product_service.get_all_batches(db=db, skip=skip, limit=limit)

@router.get("/batches/{batch_id}", response_model=schemas.Batch)
async def get_batch_by_id_endpoint(
    batch_id: int, 
    db: AsyncSession = Depends(get_db_session)
):
    """
    Mengambil detail satu batch berdasarkan ID-nya.
    """
    db_batch = await product_service.get_batch_by_id(db=db, batch_id=batch_id)
    if db_batch is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")
    return db_batch

@router.put("/batches/{batch_id}", response_model=schemas.Batch)
async def update_batch_endpoint(
    batch_id: int,
    batch_data: schemas.BatchUpdate,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Memperbarui detail dari batch yang ada.
    """
    return await product_service.update_batch(db=db, batch_id=batch_id, batch_in=batch_data)

@router.delete("/batches/{batch_id}", response_model=schemas.Batch)
async def delete_batch_endpoint(
    batch_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Menghapus batch. Akan gagal jika batch sudah memiliki alokasi.
    """
    return await product_service.delete_batch(db=db, batch_id=batch_id)


# ===================================================================
# 3. ALLOCATION ENDPOINTS
# ===================================================================

@router.post("/allocations/", response_model=schemas.Allocation, status_code=status.HTTP_201_CREATED)
async def create_allocation_endpoint(
    allocation_data: schemas.AllocationCreate, 
    db: AsyncSession = Depends(get_db_session)
):
    """
    Membuat alokasi stok dari sebuah batch.
    Ini adalah langkah kunci untuk membuat stok 'tersedia' setelah inbound.
    """
    return await product_service.create_allocation(db=db, allocation_in=allocation_data)

@router.get("/allocations/{allocation_id}", response_model=schemas.Allocation)
async def get_allocation_by_id_endpoint(
    allocation_id: int, 
    db: AsyncSession = Depends(get_db_session)
):
    """
    Mengambil detail satu alokasi stok berdasarkan ID-nya.
    """
    db_allocation = await product_service.get_allocation_by_id(db=db, allocation_id=allocation_id)
    if db_allocation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Allocation not found")
    return db_allocation

@router.put("/allocations/{allocation_id}", response_model=schemas.Allocation)
async def update_allocation_endpoint(
    allocation_id: int,
    allocation_data: schemas.AllocationUpdate,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Memperbarui alokasi yang ada.
    Service layer berisi validasi penting untuk mencegah inkonsistensi data.
    """
    return await product_service.update_allocation(db=db, allocation_id=allocation_id, allocation_in=allocation_data)

@router.delete("/allocations/{allocation_id}", response_model=schemas.Allocation)
async def delete_allocation_endpoint(
    allocation_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Menghapus alokasi. Akan gagal jika alokasi sudah ditempatkan di rak atau sudah dikirim.
    """
    return await product_service.delete_allocation(db=db, allocation_id=allocation_id)