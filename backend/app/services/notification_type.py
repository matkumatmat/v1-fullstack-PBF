from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.type import NotificationType
from app.schemas.notification_type import NotificationTypeCreate, NotificationTypeUpdate

async def get_notification_type(db: AsyncSession, notification_type_id: int):
    result = await db.execute(select(NotificationType).filter(NotificationType.id == notification_type_id))
    return result.scalar_one_or_none()

async def get_notification_types(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(NotificationType).offset(skip).limit(limit))
    return result.scalars().all()

async def create_notification_type(db: AsyncSession, notification_type: NotificationTypeCreate):
    db_notification_type = NotificationType(**notification_type.dict())
    db.add(db_notification_type)
    await db.commit()
    await db.refresh(db_notification_type)
    return db_notification_type

async def update_notification_type(db: AsyncSession, notification_type_id: int, notification_type: NotificationTypeUpdate):
    db_notification_type = await get_notification_type(db, notification_type_id)
    if db_notification_type:
        update_data = notification_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_notification_type, key, value)
        await db.commit()
        await db.refresh(db_notification_type)
    return db_notification_type

async def delete_notification_type(db: AsyncSession, notification_type_id: int):
    db_notification_type = await get_notification_type(db, notification_type_id)
    if db_notification_type:
        await db.delete(db_notification_type)
        await db.commit()
    return db_notification_type