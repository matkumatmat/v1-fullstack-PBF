from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.type import PriorityLevel
from app.schemas.priority_level import PriorityLevelCreate, PriorityLevelUpdate

async def get_priority_level(db: AsyncSession, priority_level_id: int):
    result = await db.execute(select(PriorityLevel).filter(PriorityLevel.id == priority_level_id))
    return result.scalar_one_or_none()

async def get_priority_levels(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(PriorityLevel).offset(skip).limit(limit))
    return result.scalars().all()

async def create_priority_level(db: AsyncSession, priority_level: PriorityLevelCreate):
    db_priority_level = PriorityLevel(**priority_level.dict())
    db.add(db_priority_level)
    await db.commit()
    await db.refresh(db_priority_level)
    return db_priority_level

async def update_priority_level(db: AsyncSession, priority_level_id: int, priority_level: PriorityLevelUpdate):
    db_priority_level = await get_priority_level(db, priority_level_id)
    if db_priority_level:
        update_data = priority_level.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_priority_level, key, value)
        await db.commit()
        await db.refresh(db_priority_level)
    return db_priority_level

async def delete_priority_level(db: AsyncSession, priority_level_id: int):
    db_priority_level = await get_priority_level(db, priority_level_id)
    if db_priority_level:
        await db.delete(db_priority_level)
        await db.commit()
    return db_priority_level