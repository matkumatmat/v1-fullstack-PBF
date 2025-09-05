from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.type import PackagingBoxType
from app.schemas.packaging_box_type import PackagingBoxTypeCreate, PackagingBoxTypeUpdate

async def get_packaging_box_type(db: AsyncSession, packaging_box_type_id: int):
    result = await db.execute(select(PackagingBoxType).filter(PackagingBoxType.id == packaging_box_type_id))
    return result.scalar_one_or_none()

async def get_packaging_box_types(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(PackagingBoxType).offset(skip).limit(limit))
    return result.scalars().all()

async def create_packaging_box_type(db: AsyncSession, packaging_box_type: PackagingBoxTypeCreate):
    db_packaging_box_type = PackagingBoxType(**packaging_box_type.dict())
    db.add(db_packaging_box_type)
    await db.commit()
    await db.refresh(db_packaging_box_type)
    return db_packaging_box_type

async def update_packaging_box_type(db: AsyncSession, packaging_box_type_id: int, packaging_box_type: PackagingBoxTypeUpdate):
    db_packaging_box_type = await get_packaging_box_type(db, packaging_box_type_id)
    if db_packaging_box_type:
        update_data = packaging_box_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_packaging_box_type, key, value)
        await db.commit()
        await db.refresh(db_packaging_box_type)
    return db_packaging_box_type

async def delete_packaging_box_type(db: AsyncSession, packaging_box_type_id: int):
    db_packaging_box_type = await get_packaging_box_type(db, packaging_box_type_id)
    if db_packaging_box_type:
        await db.delete(db_packaging_box_type)
        await db.commit()
    return db_packaging_box_type