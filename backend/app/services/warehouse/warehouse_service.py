from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.warehouse import Warehouse, Rack, RackAllocation
from app.schemas.warehouse.warehouse_schemas import WarehouseCreate, WarehouseUpdate,RackCreate, RackUpdate, RackAllocationCreate, RackAllocationUpdate


async def get_warehouse(db: AsyncSession, warehouse_id: int):
    result = await db.execute(select(Warehouse).filter(Warehouse.id == warehouse_id))
    return result.scalar_one_or_none()

async def get_warehouses(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Warehouse).offset(skip).limit(limit))
    return result.scalars().all()

async def create_warehouse(db: AsyncSession, warehouse: WarehouseCreate):
    db_warehouse = Warehouse(**warehouse.model_dump())
    db.add(db_warehouse)
    await db.commit()
    await db.refresh(db_warehouse)
    return db_warehouse

async def update_warehouse(db: AsyncSession, warehouse_id: int, warehouse: WarehouseUpdate):
    db_warehouse = await get_warehouse(db, warehouse_id)
    if db_warehouse:
        update_data = warehouse.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_warehouse, key, value)
        await db.commit()
        await db.refresh(db_warehouse)
    return db_warehouse

async def delete_warehouse(db: AsyncSession, warehouse_id: int):
    db_warehouse = await get_warehouse(db, warehouse_id)
    if db_warehouse:
        await db.delete(db_warehouse)
        await db.commit()
    return db_warehouse


async def get_rack(db: AsyncSession, rack_id: int):
    result = await db.execute(select(Rack).filter(Rack.id == rack_id))
    return result.scalar_one_or_none()

async def get_racks(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Rack).offset(skip).limit(limit))
    return result.scalars().all()

async def create_rack(db: AsyncSession, rack: RackCreate):
    db_rack = Rack(**rack.model_dump())
    db.add(db_rack)
    await db.commit()
    await db.refresh(db_rack)
    return db_rack

async def update_rack(db: AsyncSession, rack_id: int, rack: RackUpdate):
    db_rack = await get_rack(db, rack_id)
    if db_rack:
        update_data = rack.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_rack, key, value)
        await db.commit()
        await db.refresh(db_rack)
    return db_rack

async def delete_rack(db: AsyncSession, rack_id: int):
    db_rack = await get_rack(db, rack_id)
    if db_rack:
        await db.delete(db_rack)
        await db.commit()
    return db_rack

async def get_rack_allocation(db: AsyncSession, rack_allocation_id: int):
    result = await db.execute(select(RackAllocation).filter(RackAllocation.id == rack_allocation_id))
    return result.scalar_one_or_none()

async def get_rack_allocations(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(RackAllocation).offset(skip).limit(limit))
    return result.scalars().all()

async def create_rack_allocation(db: AsyncSession, rack_allocation: RackAllocationCreate):
    db_rack_allocation = RackAllocation(**rack_allocation.model_dump())
    db.add(db_rack_allocation)
    await db.commit()
    await db.refresh(db_rack_allocation)
    return db_rack_allocation

async def update_rack_allocation(db: AsyncSession, rack_allocation_id: int, rack_allocation: RackAllocationUpdate):
    db_rack_allocation = await get_rack_allocation(db, rack_allocation_id)
    if db_rack_allocation:
        update_data = rack_allocation.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_rack_allocation, key, value)
        await db.commit()
        await db.refresh(db_rack_allocation)
    return db_rack_allocation

async def delete_rack_allocation(db: AsyncSession, rack_allocation_id: int):
    db_rack_allocation = await get_rack_allocation(db, rack_allocation_id)
    if db_rack_allocation:
        await db.delete(db_rack_allocation)
        await db.commit()
    return db_rack_allocation