from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.type import CustomerType
from app.schemas.customer_type import CustomerTypeCreate, CustomerTypeUpdate

async def get_customer_type(db: AsyncSession, customer_type_id: int):
    result = await db.execute(select(CustomerType).filter(CustomerType.id == customer_type_id))
    return result.scalar_one_or_none()

async def get_customer_types(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(CustomerType).offset(skip).limit(limit))
    return result.scalars().all()

async def create_customer_type(db: AsyncSession, customer_type: CustomerTypeCreate):
    db_customer_type = CustomerType(**customer_type.dict())
    db.add(db_customer_type)
    await db.commit()
    await db.refresh(db_customer_type)
    return db_customer_type

async def update_customer_type(db: AsyncSession, customer_type_id: int, customer_type: CustomerTypeUpdate):
    db_customer_type = await get_customer_type(db, customer_type_id)
    if db_customer_type:
        update_data = customer_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_customer_type, key, value)
        await db.commit()
        await db.refresh(db_customer_type)
    return db_customer_type

async def delete_customer_type(db: AsyncSession, customer_type_id: int):
    db_customer_type = await get_customer_type(db, customer_type_id)
    if db_customer_type:
        await db.delete(db_customer_type)
        await db.commit()
    return db_customer_type