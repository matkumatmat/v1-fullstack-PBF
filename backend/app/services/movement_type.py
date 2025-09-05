from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.type import MovementType
from app.schemas.movement_type import MovementTypeCreate, MovementTypeUpdate

async def get_movement_type(db: AsyncSession, movement_type_id: int):
    result = await db.execute(select(MovementType).filter(MovementType.id == movement_type_id))
    return result.scalar_one_or_none()

async def get_movement_types(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(MovementType).offset(skip).limit(limit))
    return result.scalars().all()

async def create_movement_type(db: AsyncSession, movement_type: MovementTypeCreate):
    db_movement_type = MovementType(**movement_type.dict())
    db.add(db_movement_type)
    await db.commit()
    await db.refresh(db_movement_type)
    return db_movement_type

async def update_movement_type(db: AsyncSession, movement_type_id: int, movement_type: MovementTypeUpdate):
    db_movement_type = await get_movement_type(db, movement_type_id)
    if db_movement_type:
        update_data = movement_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_movement_type, key, value)
        await db.commit()
        await db.refresh(db_movement_type)
    return db_movement_type

async def delete_movement_type(db: AsyncSession, movement_type_id: int):
    db_movement_type = await get_movement_type(db, movement_type_id)
    if db_movement_type:
        await db.delete(db_movement_type)
        await db.commit()
    return db_movement_type