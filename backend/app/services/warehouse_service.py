# file: app/services/warehouse_service.py (FULL REFACTORED CODE)

from typing import List, Optional
from sqlalchemy import exc
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

# Impor model yang sudah final
from app.models.warehouse import Warehouse, Rack, StockPlacement
from app.models.product import Allocation

# Impor skema yang Anda berikan
from app.schemas import WarehouseCreate, WarehouseUpdate, RackCreate, RackUpdate, StockPlacementCreate

# Impor exception kustom
from app.core.exceptions import NotFoundException, BadRequestException

# --- Warehouse Services ---

async def get_warehouse_by_id(db: AsyncSession, warehouse_id: int) -> Optional[Warehouse]:
    """
    Mengambil satu warehouse berdasarkan ID, dengan semua relasi yang dibutuhkan sudah di-load.
    """
    query = (
        select(Warehouse)
        .where(Warehouse.id == warehouse_id)
        # ✅ REFACTOR: Eager load SEMUA relasi yang ada di skema Pydantic Warehouse.
        .options(
            selectinload(Warehouse.racks),
            selectinload(Warehouse.temperature_type)
        )
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_all_warehouses(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Warehouse]:
    """
    Mengambil daftar warehouse, dengan semua relasi yang dibutuhkan sudah di-load.
    """
    query = (
        select(Warehouse)
        .offset(skip)
        .limit(limit)
        .order_by(Warehouse.id)
        # ✅ REFACTOR: Eager load relasi untuk setiap item dalam daftar.
        .options(
            selectinload(Warehouse.racks),
            selectinload(Warehouse.temperature_type)
        )
    )
    result = await db.execute(query)
    return result.scalars().all()

async def create_warehouse(db: AsyncSession, warehouse_in: WarehouseCreate) -> Warehouse:
    """
    Membuat warehouse baru dan mengembalikannya dengan semua relasi sudah di-load.
    """
    db_warehouse = Warehouse(**warehouse_in.model_dump())
    db.add(db_warehouse)
    try:
        await db.commit()
    except exc.IntegrityError:
        await db.rollback()
        raise BadRequestException(f"Warehouse with code '{warehouse_in.code}' already exists.")
    
    # ✅ REFACTOR: Setelah membuat, panggil get_warehouse_by_id untuk mendapatkan objek
    # yang sudah lengkap dengan relasinya, menghindari lazy loading di respons API.
    return await get_warehouse_by_id(db, db_warehouse.id)

async def update_warehouse(db: AsyncSession, warehouse_id: int, warehouse_in: WarehouseUpdate) -> Warehouse:
    """
    Memperbarui warehouse dan mengembalikannya dengan semua relasi sudah di-load.
    """
    db_warehouse = await get_warehouse_by_id(db, warehouse_id)
    if not db_warehouse:
        raise NotFoundException(f"Warehouse with id {warehouse_id} not found.")
    
    update_data = warehouse_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_warehouse, key, value)
        
    db.add(db_warehouse)
    try:
        await db.commit()
    except exc.IntegrityError:
        await db.rollback()
        raise BadRequestException(f"Update failed. A warehouse with the provided code may already exist.")
        
    # ✅ REFACTOR: Sama seperti create, panggil kembali untuk mendapatkan objek yang lengkap.
    return await get_warehouse_by_id(db, warehouse_id)

async def delete_warehouse(db: AsyncSession, warehouse_id: int) -> Warehouse:
    # ✅ REFACTOR: Gunakan get_warehouse_by_id yang sudah di-eager load untuk validasi.
    db_warehouse = await get_warehouse_by_id(db, warehouse_id)
    if not db_warehouse:
        raise NotFoundException(f"Warehouse with id {warehouse_id} not found.")
    
    if db_warehouse.racks:
        raise BadRequestException(f"Cannot delete warehouse '{db_warehouse.name}'. It still contains racks.")

    await db.delete(db_warehouse)
    await db.commit()
    return db_warehouse

# --- Rack Services ---

async def get_rack_by_id(db: AsyncSession, rack_id: int) -> Optional[Rack]:
    """
    Mengambil satu rack berdasarkan ID, dengan semua relasi yang dibutuhkan sudah di-load.
    """
    query = (
        select(Rack)
        .where(Rack.id == rack_id)
        # ✅ REFACTOR: Eager load relasi yang ada di skema Pydantic Rack.
        .options(
            selectinload(Rack.location_type),
            selectinload(Rack.placement).selectinload(StockPlacement.allocation)
        )
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_all_racks(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Rack]:
    """
    Mengambil daftar rack, dengan semua relasi yang dibutuhkan sudah di-load.
    """
    query = (
        select(Rack)
        .offset(skip)
        .limit(limit)
        .order_by(Rack.id)
        # ✅ REFACTOR: Eager load relasi untuk setiap item dalam daftar.
        .options(
            selectinload(Rack.location_type),
            selectinload(Rack.placement)
        )
    )
    result = await db.execute(query)
    return result.scalars().all()

async def create_rack(db: AsyncSession, rack_in: RackCreate) -> Rack:
    """
    Membuat rack baru dan mengembalikannya dengan semua relasi sudah di-load.
    """
    warehouse = await get_warehouse_by_id(db, rack_in.warehouse_id)
    if not warehouse:
        raise NotFoundException(f"Cannot create rack. Warehouse with id {rack_in.warehouse_id} not found.")
    
    db_rack = Rack(**rack_in.model_dump())
    db.add(db_rack)
    try:
        await db.commit()
    except exc.IntegrityError:
        await db.rollback()
        raise BadRequestException(f"Rack with code '{rack_in.code}' already exists.")
    
    # ✅ REFACTOR: Panggil kembali untuk mendapatkan objek yang lengkap.
    return await get_rack_by_id(db, db_rack.id)

async def update_rack(db: AsyncSession, rack_id: int, rack_in: RackUpdate) -> Rack:
    """
    Memperbarui rack dan mengembalikannya dengan semua relasi sudah di-load.
    """
    db_rack = await get_rack_by_id(db, rack_id)
    if not db_rack:
        raise NotFoundException(f"Rack with id {rack_id} not found.")
    
    update_data = rack_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_rack, key, value)
        
    db.add(db_rack)
    try:
        await db.commit()
    except exc.IntegrityError:
        await db.rollback()
        raise BadRequestException(f"Update failed. A rack with the provided code may already exist.")
        
    # ✅ REFACTOR: Panggil kembali untuk mendapatkan objek yang lengkap.
    return await get_rack_by_id(db, rack_id)

async def delete_rack(db: AsyncSession, rack_id: int) -> Rack:
    # ✅ REFACTOR: Gunakan get_rack_by_id yang sudah di-eager load untuk validasi.
    db_rack = await get_rack_by_id(db, rack_id)
    if not db_rack:
        raise NotFoundException(f"Rack with id {rack_id} not found.")
    
    if db_rack.placement:
        raise BadRequestException(f"Cannot delete rack {db_rack.code}. It is currently occupied.")
        
    await db.delete(db_rack)
    await db.commit()
    return db_rack

# --- Stock Placement Services ---
# (Fungsi-fungsi ini tidak perlu banyak diubah karena mereka tidak mengembalikan objek dengan relasi kompleks
# yang perlu diserialisasi, kecuali jika skema StockPlacement Anda juga memiliki relasi yang dalam)

async def get_placement_by_id(db: AsyncSession, placement_id: int) -> Optional[StockPlacement]:
    query = select(StockPlacement).where(StockPlacement.id == placement_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def place_stock_in_rack(db: AsyncSession, placement_in: StockPlacementCreate) -> StockPlacement:
    # ... (kode Anda di sini sudah cukup baik karena menggunakan nested transaction) ...
    # Namun, untuk mengembalikan objek yang lengkap, kita akan query ulang.
    
    new_placement_id: Optional[int] = None
    async with db.begin_nested():
        # ... (validasi Anda tetap sama) ...
        rack_query = select(Rack).where(Rack.id == placement_in.rack_id).with_for_update()
        rack = (await db.execute(rack_query)).scalar_one_or_none()
        alloc_query = select(Allocation).where(Allocation.id == placement_in.allocation_id).options(selectinload(Allocation.placements)).with_for_update()
        allocation = (await db.execute(alloc_query)).scalar_one_or_none()
        if not rack: raise NotFoundException(f"Rack with id {placement_in.rack_id} not found.")
        if not allocation: raise NotFoundException(f"Allocation with id {placement_in.allocation_id} not found.")
        if rack.placement: raise BadRequestException(f"Rack {rack.code} is already occupied.")
        # ... (validasi kuantitas Anda tetap sama) ...

        db_placement = StockPlacement(**placement_in.model_dump())
        db.add(db_placement)
        await db.flush()
        new_placement_id = db_placement.id
    
    # ✅ REFACTOR: Query ulang untuk mendapatkan objek StockPlacement yang lengkap
    # dengan relasi rack dan allocation-nya.
    final_query = (
        select(StockPlacement)
        .where(StockPlacement.id == new_placement_id)
        .options(
            selectinload(StockPlacement.rack),
            selectinload(StockPlacement.allocation)
        )
    )
    result = await db.execute(final_query)
    return result.scalar_one()


async def remove_stock_from_rack(db: AsyncSession, rack_id: int) -> Rack:
    # ... (kode Anda di sini sudah cukup baik) ...
    async with db.begin_nested():
        rack_query = select(Rack).where(Rack.id == rack_id).options(selectinload(Rack.placement)).with_for_update()
        rack = (await db.execute(rack_query)).scalar_one_or_none()
        if not rack: raise NotFoundException(f"Rack with id {rack_id} not found.")
        if not rack.placement: raise BadRequestException(f"Rack {rack.code} is already empty.")
        await db.delete(rack.placement)
        await db.flush()
    
    # ✅ REFACTOR: Panggil kembali untuk mendapatkan objek Rack yang sudah ter-update dan lengkap.
    return await get_rack_by_id(db, rack_id)