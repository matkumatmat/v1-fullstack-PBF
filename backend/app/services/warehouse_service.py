# file: app/services/warehouse_service.py

from typing import List, Optional
from sqlalchemy import exc
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

# Impor model yang sudah final
from app.models.warehouse import Warehouse, Rack, StockPlacement
from app.models.product import Allocation

# Impor skema yang Anda berikan
from app.schemas.warehouse import WarehouseCreate, WarehouseUpdate, RackCreate, RackUpdate, StockPlacementCreate


# Impor exception kustom
from app.core.exceptions import NotFoundException, BadRequestException

# --- Warehouse Services ---

async def get_warehouse_by_id(db: AsyncSession, warehouse_id: int) -> Optional[Warehouse]:
    query = select(Warehouse).where(Warehouse.id == warehouse_id).options(selectinload(Warehouse.racks))
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_all_warehouses(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Warehouse]:
    query = select(Warehouse).offset(skip).limit(limit).options(selectinload(Warehouse.racks))
    result = await db.execute(query)
    return result.scalars().all()

async def create_warehouse(db: AsyncSession, warehouse_in: WarehouseCreate) -> Warehouse:
    # Menggunakan **model_dump() di sini bisa diterima karena skema Create sangat terbatas
    # dan tidak ada nilai default server yang signifikan yang bisa tertimpa.
    db_warehouse = Warehouse(**warehouse_in.model_dump())
    db.add(db_warehouse)
    try:
        await db.commit()
    except exc.IntegrityError:
        await db.rollback()
        raise BadRequestException(f"Warehouse with code '{warehouse_in.code}' already exists.")
    await db.refresh(db_warehouse)
    return db_warehouse

async def update_warehouse(db: AsyncSession, warehouse_id: int, warehouse_in: WarehouseUpdate) -> Warehouse:
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
        
    await db.refresh(db_warehouse)
    return db_warehouse

async def delete_warehouse(db: AsyncSession, warehouse_id: int) -> Warehouse:
    db_warehouse = await get_warehouse_by_id(db, warehouse_id)
    if not db_warehouse:
        raise NotFoundException(f"Warehouse with id {warehouse_id} not found.")
    
    # Tambahkan validasi: tidak bisa menghapus gudang jika masih ada rak di dalamnya
    if db_warehouse.racks:
        raise BadRequestException(f"Cannot delete warehouse '{db_warehouse.name}'. It still contains racks.")

    await db.delete(db_warehouse)
    await db.commit()
    return db_warehouse

# --- Rack Services ---

async def get_rack_by_id(db: AsyncSession, rack_id: int) -> Optional[Rack]:
    query = (
        select(Rack)
        .where(Rack.id == rack_id)
        .options(
            selectinload(Rack.placement)
            .joinedload(StockPlacement.allocation)
        )
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_all_racks(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Rack]:
    query = select(Rack).offset(skip).limit(limit).options(selectinload(Rack.placement))
    result = await db.execute(query)
    return result.scalars().all()

async def create_rack(db: AsyncSession, rack_in: RackCreate) -> Rack:
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
    await db.refresh(db_rack)
    return db_rack

async def update_rack(db: AsyncSession, rack_id: int, rack_in: RackUpdate) -> Rack:
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
        
    await db.refresh(db_rack)
    return db_rack

async def delete_rack(db: AsyncSession, rack_id: int) -> Rack:
    db_rack = await get_rack_by_id(db, rack_id)
    if not db_rack:
        raise NotFoundException(f"Rack with id {rack_id} not found.")
    
    if db_rack.placement:
        raise BadRequestException(f"Cannot delete rack {db_rack.code}. It is currently occupied.")
        
    await db.delete(db_rack)
    await db.commit()
    return db_rack

# --- Stock Placement Services ---

async def get_placement_by_id(db: AsyncSession, placement_id: int) -> Optional[StockPlacement]:
    query = select(StockPlacement).where(StockPlacement.id == placement_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def place_stock_in_rack(db: AsyncSession, placement_in: StockPlacementCreate) -> StockPlacement:
    async with db.begin_nested():
        rack_query = select(Rack).where(Rack.id == placement_in.rack_id).with_for_update()
        rack = (await db.execute(rack_query)).scalar_one_or_none()

        alloc_query = select(Allocation).where(Allocation.id == placement_in.allocation_id).options(selectinload(Allocation.placements)).with_for_update()
        allocation = (await db.execute(alloc_query)).scalar_one_or_none()

        if not rack:
            raise NotFoundException(f"Rack with id {placement_in.rack_id} not found.")
        if not allocation:
            raise NotFoundException(f"Allocation with id {placement_in.allocation_id} not found.")
        if rack.placement:
             raise BadRequestException(f"Rack {rack.code} is already occupied.")

        ### INI ADALAH VALIDASI YANG BENAR DAN LENGKAP ###
        if placement_in.quantity > rack.capacity:
            raise BadRequestException(f"Cannot place {placement_in.quantity} units. Rack {rack.code} only has a capacity of {rack.capacity}.")

        total_placed_quantity = sum(p.quantity for p in allocation.placements)
        available_to_place = allocation.allocated_quantity - total_placed_quantity
        
        if placement_in.quantity > available_to_place:
            raise BadRequestException(f"Cannot place {placement_in.quantity} units. Only {available_to_place} units are available in allocation {allocation.id}.")

        db_placement = StockPlacement(**placement_in.model_dump())
        db.add(db_placement)
        
        await db.flush()
        await db.refresh(db_placement)
        
    return db_placement

async def remove_stock_from_rack(db: AsyncSession, rack_id: int) -> Rack:
    async with db.begin_nested():
        rack_query = select(Rack).where(Rack.id == rack_id).options(selectinload(Rack.placement)).with_for_update()
        rack = (await db.execute(rack_query)).scalar_one_or_none()

        if not rack:
            raise NotFoundException(f"Rack with id {rack_id} not found.")
        
        if not rack.placement:
            raise BadRequestException(f"Rack {rack.code} is already empty.")

        await db.delete(rack.placement)
        await db.flush()
        await db.refresh(rack)
        
    return rack