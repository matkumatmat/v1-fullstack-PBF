from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db_session
from app.schemas.product_price import ProductPrice, ProductPriceCreate, ProductPriceUpdate
import app.services.product_price as product_price_service

router = APIRouter()

@router.post("/", response_model=ProductPrice)
async def create_product_price(
    product_price: ProductPriceCreate, db: AsyncSession = Depends(get_db_session)
):
    return await product_price_service.create_product_price(db=db, product_price=product_price)

@router.get("/", response_model=List[ProductPrice])
async def read_product_prices(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)
):
    product_prices = await product_price_service.get_product_prices(db, skip=skip, limit=limit)
    return product_prices

@router.get("/{product_price_id}", response_model=ProductPrice)
async def read_product_price(product_price_id: int, db: AsyncSession = Depends(get_db_session)):
    db_product_price = await product_price_service.get_product_price(db, product_price_id=product_price_id)
    if db_product_price is None:
        raise HTTPException(status_code=404, detail="ProductPrice not found")
    return db_product_price

@router.put("/{product_price_id}", response_model=ProductPrice)
async def update_product_price(
    product_price_id: int,
    product_price: ProductPriceUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    db_product_price = await product_price_service.update_product_price(
        db, product_price_id=product_price_id, product_price=product_price
    )
    if db_product_price is None:
        raise HTTPException(status_code=404, detail="ProductPrice not found")
    return db_product_price

@router.delete("/{product_price_id}", response_model=ProductPrice)
async def delete_product_price(
    product_price_id: int, db: AsyncSession = Depends(get_db_session)
):
    db_product_price = await product_price_service.delete_product_price(db, product_price_id=product_price_id)
    if db_product_price is None:
        raise HTTPException(status_code=404, detail="ProductPrice not found")
    return db_product_price