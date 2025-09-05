from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db_session
from app.schemas.delivery_type import DeliveryType, DeliveryTypeCreate, DeliveryTypeUpdate
import app.services.delivery_type as delivery_type_service

router = APIRouter()

@router.post("/", response_model=DeliveryType)
async def create_delivery_type(
    delivery_type: DeliveryTypeCreate, db: AsyncSession = Depends(get_db_session)
):
    return await delivery_type_service.create_delivery_type(db=db, delivery_type=delivery_type)

@router.get("/", response_model=List[DeliveryType])
async def read_delivery_types(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)
):
    delivery_types = await delivery_type_service.get_delivery_types(db, skip=skip, limit=limit)
    return delivery_types

@router.get("/{delivery_type_id}", response_model=DeliveryType)
async def read_delivery_type(delivery_type_id: int, db: AsyncSession = Depends(get_db_session)):
    db_delivery_type = await delivery_type_service.get_delivery_type(db, delivery_type_id=delivery_type_id)
    if db_delivery_type is None:
        raise HTTPException(status_code=404, detail="DeliveryType not found")
    return db_delivery_type

@router.put("/{delivery_type_id}", response_model=DeliveryType)
async def update_delivery_type(
    delivery_type_id: int,
    delivery_type: DeliveryTypeUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    db_delivery_type = await delivery_type_service.update_delivery_type(
        db, delivery_type_id=delivery_type_id, delivery_type=delivery_type
    )
    if db_delivery_type is None:
        raise HTTPException(status_code=404, detail="DeliveryType not found")
    return db_delivery_type

@router.delete("/{delivery_type_id}", response_model=DeliveryType)
async def delete_delivery_type(
    delivery_type_id: int, db: AsyncSession = Depends(get_db_session)
):
    db_delivery_type = await delivery_type_service.delete_delivery_type(db, delivery_type_id=delivery_type_id)
    if db_delivery_type is None:
        raise HTTPException(status_code=404, detail="DeliveryType not found")
    return db_delivery_type