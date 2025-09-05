from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.type import TemperatureType
from app.schemas.temperature_type import TemperatureTypeCreate, TemperatureTypeUpdate

async def get_temperature_type(db: AsyncSession, temperature_type_id: int):
    result = await db.execute(select(TemperatureType).filter(TemperatureType.id == temperature_type_id))
    return result.scalar_one_or_none()

async def get_temperature_types(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(TemperatureType).offset(skip).limit(limit))
    return result.scalars().all()

async def create_temperature_type(db: AsyncSession, temperature_type: TemperatureTypeCreate):
    db_temperature_type = TemperatureType(**temperature_type.dict())
    db.add(db_temperature_type)
    await db.commit()
    await db.refresh(db_temperature_type)
    return db_temperature_type

async def update_temperature_type(db: AsyncSession, temperature_type_id: int, temperature_type: TemperatureTypeUpdate):
    db_temperature_type = await get_temperature_type(db, temperature_type_id)
    if db_temperature_type:
        update_data = temperature_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_temperature_type, key, value)
        await db.commit()
        await db.refresh(db_temperature_type)
    return db_temperature_type

async def delete_temperature_type(db: AsyncSession, temperature_type_id: int):
    db_temperature_type = await get_temperature_type(db, temperature_type_id)
    if db_temperature_type:
        await db.delete(db_temperature_type)
        await db.commit()
    return db_temperature_type