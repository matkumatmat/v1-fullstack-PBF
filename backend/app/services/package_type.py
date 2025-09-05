from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.type import PackageType
from app.schemas.package_type import PackageTypeCreate, PackageTypeUpdate

async def get_package_type(db: AsyncSession, package_type_id: int):
    result = await db.execute(select(PackageType).filter(PackageType.id == package_type_id))
    return result.scalar_one_or_none()

async def get_package_types(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(PackageType).offset(skip).limit(limit))
    return result.scalars().all()

async def create_package_type(db: AsyncSession, package_type: PackageTypeCreate):
    db_package_type = PackageType(**package_type.dict())
    db.add(db_package_type)
    await db.commit()
    await db.refresh(db_package_type)
    return db_package_type

async def update_package_type(db: AsyncSession, package_type_id: int, package_type: PackageTypeUpdate):
    db_package_type = await get_package_type(db, package_type_id)
    if db_package_type:
        update_data = package_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_package_type, key, value)
        await db.commit()
        await db.refresh(db_package_type)
    return db_package_type

async def delete_package_type(db: AsyncSession, package_type_id: int):
    db_package_type = await get_package_type(db, package_type_id)
    if db_package_type:
        await db.delete(db_package_type)
        await db.commit()
    return db_package_type