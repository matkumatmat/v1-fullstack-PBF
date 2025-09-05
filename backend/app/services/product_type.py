from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.type import ProductType
from app.schemas.product_type import ProductTypeCreate, ProductTypeUpdate

async def get_product_type(db: AsyncSession, product_type_id: int):
    result = await db.execute(select(ProductType).filter(ProductType.id == product_type_id))
    return result.scalar_one_or_none()

async def get_product_types(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(ProductType).offset(skip).limit(limit))
    return result.scalars().all()

async def create_product_type(db: AsyncSession, product_type: ProductTypeCreate):
    db_product_type = ProductType(**product_type.dict())
    db.add(db_product_type)
    await db.commit()
    await db.refresh(db_product_type)
    return db_product_type

async def update_product_type(db: AsyncSession, product_type_id: int, product_type: ProductTypeUpdate):
    db_product_type = await get_product_type(db, product_type_id)
    if db_product_type:
        update_data = product_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product_type, key, value)
        await db.commit()
        await db.refresh(db_product_type)
    return db_product_type

async def delete_product_type(db: AsyncSession, product_type_id: int):
    db_product_type = await get_product_type(db, product_type_id)
    if db_product_type:
        await db.delete(db_product_type)
        await db.commit()
    return db_product_type