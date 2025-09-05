from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.type import SectorType
from app.schemas.sector_type import SectorTypeCreate, SectorTypeUpdate

async def get_sector_type(db: AsyncSession, sector_type_id: int):
    result = await db.execute(select(SectorType).filter(SectorType.id == sector_type_id))
    return result.scalar_one_or_none()

async def get_sector_types(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(SectorType).offset(skip).limit(limit))
    return result.scalars().all()

async def create_sector_type(db: AsyncSession, sector_type: SectorTypeCreate):
    db_sector_type = SectorType(**sector_type.dict())
    db.add(db_sector_type)
    await db.commit()
    await db.refresh(db_sector_type)
    return db_sector_type

async def update_sector_type(db: AsyncSession, sector_type_id: int, sector_type: SectorTypeUpdate):
    db_sector_type = await get_sector_type(db, sector_type_id)
    if db_sector_type:
        update_data = sector_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_sector_type, key, value)
        await db.commit()
        await db.refresh(db_sector_type)
    return db_sector_type

async def delete_sector_type(db: AsyncSession, sector_type_id: int):
    db_sector_type = await get_sector_type(db, sector_type_id)
    if db_sector_type:
        await db.delete(db_sector_type)
        await db.commit()
    return db_sector_type