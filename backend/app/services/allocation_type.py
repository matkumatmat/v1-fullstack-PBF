from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.type import AllocationType
from app.schemas.allocation_type import AllocationTypeCreate, AllocationTypeUpdate

async def get_allocation_type(db: AsyncSession, allocation_type_id: int):
    result = await db.execute(select(AllocationType).filter(AllocationType.id == allocation_type_id))
    return result.scalar_one_or_none()

async def get_allocation_types(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(AllocationType).offset(skip).limit(limit))
    return result.scalars().all()

async def create_allocation_type(db: AsyncSession, allocation_type: AllocationTypeCreate):
    db_allocation_type = AllocationType(**allocation_type.dict())
    db.add(db_allocation_type)
    await db.commit()
    await db.refresh(db_allocation_type)
    return db_allocation_type

async def update_allocation_type(db: AsyncSession, allocation_type_id: int, allocation_type: AllocationTypeUpdate):
    db_allocation_type = await get_allocation_type(db, allocation_type_id)
    if db_allocation_type:
        update_data = allocation_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_allocation_type, key, value)
        await db.commit()
        await db.refresh(db_allocation_type)
    return db_allocation_type

async def delete_allocation_type(db: AsyncSession, allocation_type_id: int):
    db_allocation_type = await get_allocation_type(db, allocation_type_id)
    if db_allocation_type:
        await db.delete(db_allocation_type)
        await db.commit()
    return db_allocation_type