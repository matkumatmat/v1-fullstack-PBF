from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db_session
from app.schemas.delivery_type import DeliveryType, DeliveryTypeCreate, DeliveryTypeUpdate
from app.services.delivery_type import (
    create_delivery_type,
    delete_delivery_type,
    get_delivery_type,
    get_delivery_types,
    update_delivery_type,
)

router = APIRouter()

@router.post("/", response_model=DeliveryType)
def create_new_delivery_type(
    delivery_type: DeliveryTypeCreate, db: Session = Depends(get_db_session)
):
    return create_delivery_type(db=db, delivery_type=delivery_type)

@router.get("/{delivery_type_id}", response_model=DeliveryType)
def read_delivery_type(delivery_type_id: int, db: Session = Depends(get_db_session)):
    db_delivery_type = get_delivery_type(db, delivery_type_id=delivery_type_id)
    if db_delivery_type is None:
        raise HTTPException(status_code=404, detail="DeliveryType not found")
    return db_delivery_type

@router.get("/", response_model=List[DeliveryType])
def read_delivery_types(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)
):
    delivery_types = get_delivery_types(db, skip=skip, limit=limit)
    return delivery_types

@router.put("/{delivery_type_id}", response_model=DeliveryType)
def update_existing_delivery_type(
    delivery_type_id: int,
    delivery_type: DeliveryTypeUpdate,
    db: Session = Depends(get_db_session),
):
    db_delivery_type = update_delivery_type(
        db, delivery_type_id=delivery_type_id, delivery_type=delivery_type
    )
    if db_delivery_type is None:
        raise HTTPException(status_code=404, detail="DeliveryType not found")
    return db_delivery_type

@router.delete("/{delivery_type_id}", response_model=DeliveryType)
def delete_existing_delivery_type(
    delivery_type_id: int, db: Session = Depends(get_db_session)
):
    db_delivery_type = delete_delivery_type(db, delivery_type_id=delivery_type_id)
    if db_delivery_type is None:
        raise HTTPException(status_code=404, detail="DeliveryType not found")
    return db_delivery_type
