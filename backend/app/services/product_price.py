from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.type import ProductPrice
from app.schemas.product_price import ProductPriceCreate, ProductPriceUpdate

async def get_product_price(db: AsyncSession, product_price_id: int):
    result = await db.execute(select(ProductPrice).filter(ProductPrice.id == product_price_id))
    return result.scalar_one_or_none()

async def get_product_prices(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(ProductPrice).offset(skip).limit(limit))
    return result.scalars().all()

async def create_product_price(db: AsyncSession, product_price: ProductPriceCreate):
    db_product_price = ProductPrice(**product_price.dict())
    db.add(db_product_price)
    await db.commit()
    await db.refresh(db_product_price)
    return db_product_price

async def update_product_price(db: AsyncSession, product_price_id: int, product_price: ProductPriceUpdate):
    db_product_price = await get_product_price(db, product_price_id)
    if db_product_price:
        update_data = product_price.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product_price, key, value)
        await db.commit()
        await db.refresh(db_product_price)
    return db_product_price

async def delete_product_price(db: AsyncSession, product_price_id: int):
    db_product_price = await get_product_price(db, product_price_id)
    if db_product_price:
        await db.delete(db_product_price)
        await db.commit()
    return db_product_price