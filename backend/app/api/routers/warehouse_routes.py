# file: app/api/routers/warehouse.py (FINAL REFACTORED CODE)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# --- Impor Dependensi, Skema, dan Service ---
from app.api.deps import get_db_session
from app import schemas
from app.services import warehouse_service

# --- Router Utama untuk Modul Warehouse ---
router = APIRouter()

# ===================================================================
# 1. WAREHOUSE ENDPOINTS
# ===================================================================

@router.post("/warehouses", response_model=schemas.Warehouse, status_code=status.HTTP_201_CREATED, tags=["Warehouses"])
async def create_warehouse_endpoint(warehouse_data: schemas.WarehouseCreate, db: AsyncSession = Depends(get_db_session)):
    """
    Membuat warehouse baru.
    """
    # Memastikan keyword argument 'warehouse_in' cocok dengan definisi di service.
    return await warehouse_service.create_warehouse(db=db, warehouse_in=warehouse_data)

@router.get("/warehouses", response_model=List[schemas.Warehouse], tags=["Warehouses"])
async def read_warehouses_endpoint(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)):
    """
    Mengambil daftar semua warehouse.
    """
    return await warehouse_service.get_all_warehouses(db, skip=skip, limit=limit)

@router.get("/warehouses/{warehouse_id}", response_model=schemas.Warehouse, tags=["Warehouses"])
async def read_warehouse_endpoint(warehouse_id: int, db: AsyncSession = Depends(get_db_session)):
    """
    Mengambil satu warehouse berdasarkan ID.
    """
    db_warehouse = await warehouse_service.get_warehouse_by_id(db, warehouse_id=warehouse_id)
    if db_warehouse is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found")
    return db_warehouse

@router.put("/warehouses/{warehouse_id}", response_model=schemas.Warehouse, tags=["Warehouses"])
async def update_warehouse_endpoint(warehouse_id: int, warehouse_data: schemas.WarehouseUpdate, db: AsyncSession = Depends(get_db_session)):
    """
    Memperbarui data warehouse.
    """
    # Memastikan keyword argument 'warehouse_in' cocok dengan definisi di service.
    return await warehouse_service.update_warehouse(db=db, warehouse_id=warehouse_id, warehouse_in=warehouse_data)

@router.delete("/warehouses/{warehouse_id}", response_model=schemas.Warehouse, tags=["Warehouses"])
async def delete_warehouse_endpoint(warehouse_id: int, db: AsyncSession = Depends(get_db_session)):
    """
    Menghapus warehouse.
    """
    return await warehouse_service.delete_warehouse(db, warehouse_id=warehouse_id)


# ===================================================================
# 2. RACK ENDPOINTS
# ===================================================================

@router.post("/racks", response_model=schemas.Rack, status_code=status.HTTP_201_CREATED, tags=["Racks"])
async def create_rack_endpoint(rack_data: schemas.RackCreate, db: AsyncSession = Depends(get_db_session)):
    """
    Membuat rack baru di dalam sebuah warehouse.
    """
    # Memastikan keyword argument 'rack_in' cocok dengan definisi di service.
    return await warehouse_service.create_rack(db=db, rack_in=rack_data)

@router.get("/racks", response_model=List[schemas.Rack], tags=["Racks"])
async def read_racks_endpoint(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)):
    """
    Mengambil daftar semua rack.
    """
    return await warehouse_service.get_all_racks(db, skip=skip, limit=limit)

@router.get("/racks/{rack_id}", response_model=schemas.Rack, tags=["Racks"])
async def read_rack_endpoint(rack_id: int, db: AsyncSession = Depends(get_db_session)):
    """
    Mengambil satu rack berdasarkan ID.
    """
    db_rack = await warehouse_service.get_rack_by_id(db, rack_id=rack_id)
    if db_rack is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rack not found")
    return db_rack

@router.put("/racks/{rack_id}", response_model=schemas.Rack, tags=["Racks"])
async def update_rack_endpoint(rack_id: int, rack_data: schemas.RackUpdate, db: AsyncSession = Depends(get_db_session)):
    """
    Memperbarui data rack.
    """
    # Memastikan keyword argument 'rack_in' cocok dengan definisi di service.
    return await warehouse_service.update_rack(db=db, rack_id=rack_id, rack_in=rack_data)

@router.delete("/racks/{rack_id}", response_model=schemas.Rack, tags=["Racks"])
async def delete_rack_endpoint(rack_id: int, db: AsyncSession = Depends(get_db_session)):
    """
    Menghapus rack.
    """
    return await warehouse_service.delete_rack(db, rack_id=rack_id)


# ===================================================================
# 3. STOCK PLACEMENT ENDPOINTS
# ===================================================================

@router.post("/stock-placements", response_model=schemas.StockPlacement, status_code=status.HTTP_201_CREATED, tags=["Stock Placements"])
async def place_stock_endpoint(placement_data: schemas.StockPlacementCreate, db: AsyncSession = Depends(get_db_session)):
    """
    Menempatkan stok (dari alokasi) ke dalam sebuah rack.
    """
    # Memastikan keyword argument 'placement_in' cocok dengan definisi di service.
    return await warehouse_service.place_stock_in_rack(db=db, placement_in=placement_data)

@router.delete("/racks/{rack_id}/stock-placement", response_model=schemas.Rack, tags=["Stock Placements"])
async def remove_stock_endpoint(rack_id: int, db: AsyncSession = Depends(get_db_session)):
    """
    Mengosongkan sebuah rack dengan menghapus penempatan stoknya.
    """
    return await warehouse_service.remove_stock_from_rack(db=db, rack_id=rack_id)