from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.type import LocationType
from app.schemas.location_type import LocationTypeCreate, LocationTypeUpdate

async def get_location_type(db: AsyncSession, location_type_id: int):
    result = await db.execute(select(LocationType).filter(LocationType.id == location_type_id))
    return result.scalar_one_or_none()

async def get_location_types(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(LocationType).offset(skip).limit(limit))
    return result.scalars().all()

async def create_location_type(db: AsyncSession, location_type: LocationTypeCreate):
    db_location_type = LocationType(**location_type.dict())
    db.add(db_location_type)
    await db.commit()
    await db.refresh(db_location_type)
    return db_location_type

async def update_location_type(db: AsyncSession, location_type_id: int, location_type: LocationTypeUpdate):
    db_location_type = await get_location_type(db, location_type_id)
    if db_location_type:
        update_data = location_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_location_type, key, value)
        await db.commit()
        await db.refresh(db_location_type)
    return db_location_type

async def delete_location_type(db: AsyncSession, location_type_id: int):
    db_location_type = await get_location_type(db, location_type_id)
    if db_location_type:
        await db.delete(db_location_type)
        await db.commit()
    return db_location_type