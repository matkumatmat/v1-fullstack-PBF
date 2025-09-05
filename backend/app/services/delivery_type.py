from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.type import DeliveryType
from app.schemas.delivery_type import DeliveryTypeCreate, DeliveryTypeUpdate

async def get_delivery_type(db: AsyncSession, delivery_type_id: int):
    result = await db.execute(select(DeliveryType).filter(DeliveryType.id == delivery_type_id))
    return result.scalar_one_or_none()

async def get_delivery_types(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(DeliveryType).offset(skip).limit(limit))
    return result.scalars().all()

async def create_delivery_type(db: AsyncSession, delivery_type: DeliveryTypeCreate):
    db_delivery_type = DeliveryType(**delivery_type.dict())
    db.add(db_delivery_type)
    await db.commit()
    await db.refresh(db_delivery_type)
    return db_delivery_type

async def update_delivery_type(db: AsyncSession, delivery_type_id: int, delivery_type: DeliveryTypeUpdate):
    db_delivery_type = await get_delivery_type(db, delivery_type_id)
    if db_delivery_type:
        update_data = delivery_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_delivery_type, key, value)
        await db.commit()
        await db.refresh(db_delivery_type)
    return db_delivery_type

async def delete_delivery_type(db: AsyncSession, delivery_type_id: int):
    db_delivery_type = await get_delivery_type(db, delivery_type_id)
    if db_delivery_type:
        await db.delete(db_delivery_type)
        await db.commit()
    return db_delivery_type