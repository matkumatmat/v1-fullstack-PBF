from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.type import PackagingMaterial
from app.schemas.packaging_material import PackagingMaterialCreate, PackagingMaterialUpdate

async def get_packaging_material(db: AsyncSession, packaging_material_id: int):
    result = await db.execute(select(PackagingMaterial).filter(PackagingMaterial.id == packaging_material_id))
    return result.scalar_one_or_none()

async def get_packaging_materials(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(PackagingMaterial).offset(skip).limit(limit))
    return result.scalars().all()

async def create_packaging_material(db: AsyncSession, packaging_material: PackagingMaterialCreate):
    db_packaging_material = PackagingMaterial(**packaging_material.dict())
    db.add(db_packaging_material)
    await db.commit()
    await db.refresh(db_packaging_material)
    return db_packaging_material

async def update_packaging_material(db: AsyncSession, packaging_material_id: int, packaging_material: PackagingMaterialUpdate):
    db_packaging_material = await get_packaging_material(db, packaging_material_id)
    if db_packaging_material:
        update_data = packaging_material.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_packaging_material, key, value)
        await db.commit()
        await db.refresh(db_packaging_material)
    return db_packaging_material

async def delete_packaging_material(db: AsyncSession, packaging_material_id: int):
    db_packaging_material = await get_packaging_material(db, packaging_material_id)
    if db_packaging_material:
        await db.delete(db_packaging_material)
        await db.commit()
    return db_packaging_material