from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db_session
from app.schemas.product_type import ProductType, ProductTypeCreate, ProductTypeUpdate
import app.services.product_type as product_type_service

router = APIRouter()

@router.post("/", response_model=ProductType)
async def create_product_type(
    product_type: ProductTypeCreate, db: AsyncSession = Depends(get_db_session)
):
    return await product_type_service.create_product_type(db=db, product_type=product_type)

@router.get("/", response_model=List[ProductType])
async def read_product_types(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)
):
    product_types = await product_type_service.get_product_types(db, skip=skip, limit=limit)
    return product_types

@router.get("/{product_type_id}", response_model=ProductType)
async def read_product_type(product_type_id: int, db: AsyncSession = Depends(get_db_session)):
    db_product_type = await product_type_service.get_product_type(db, product_type_id=product_type_id)
    if db_product_type is None:
        raise HTTPException(status_code=404, detail="ProductType not found")
    return db_product_type

@router.put("/{product_type_id}", response_model=ProductType)
async def update_product_type(
    product_type_id: int,
    product_type: ProductTypeUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    db_product_type = await product_type_service.update_product_type(
        db, product_type_id=product_type_id, product_type=product_type
    )
    if db_product_type is None:
        raise HTTPException(status_code=404, detail="ProductType not found")
    return db_product_type

@router.delete("/{product_type_id}", response_model=ProductType)
async def delete_product_type(
    product_type_id: int, db: AsyncSession = Depends(get_db_session)
):
    db_product_type = await product_type_service.delete_product_type(db, product_type_id=product_type_id)
    if db_product_type is None:
        raise HTTPException(status_code=404, detail="ProductType not found")
    return db_product_type