from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.type import StatusType
from app.schemas.status_type import StatusTypeCreate, StatusTypeUpdate

async def get_status_type(db: AsyncSession, status_type_id: int):
    result = await db.execute(select(StatusType).filter(StatusType.id == status_type_id))
    return result.scalar_one_or_none()

async def get_status_types(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(StatusType).offset(skip).limit(limit))
    return result.scalars().all()

async def create_status_type(db: AsyncSession, status_type: StatusTypeCreate):
    db_status_type = StatusType(**status_type.dict())
    db.add(db_status_type)
    await db.commit()
    await db.refresh(db_status_type)
    return db_status_type

async def update_status_type(db: AsyncSession, status_type_id: int, status_type: StatusTypeUpdate):
    db_status_type = await get_status_type(db, status_type_id)
    if db_status_type:
        update_data = status_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_status_type, key, value)
        await db.commit()
        await db.refresh(db_status_type)
    return db_status_type

async def delete_status_type(db: AsyncSession, status_type_id: int):
    db_status_type = await get_status_type(db, status_type_id)
    if db_status_type:
        await db.delete(db_status_type)
        await db.commit()
    return db_status_type