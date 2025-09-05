from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db_session
from app.schemas.customer_type import CustomerType, CustomerTypeCreate, CustomerTypeUpdate
from app.services.customer_type import (
    create_customer_type,
    delete_customer_type,
    get_customer_type,
    get_customer_types,
    update_customer_type,
)

router = APIRouter()

@router.post("/", response_model=CustomerType)
def create_new_customer_type(
    customer_type: CustomerTypeCreate, db: Session = Depends(get_db_session)
):
    return create_customer_type(db=db, customer_type=customer_type)

@router.get("/{customer_type_id}", response_model=CustomerType)
def read_customer_type(customer_type_id: int, db: Session = Depends(get_db_session)):
    db_customer_type = get_customer_type(db, customer_type_id=customer_type_id)
    if db_customer_type is None:
        raise HTTPException(status_code=404, detail="CustomerType not found")
    return db_customer_type

@router.get("/", response_model=List[CustomerType])
def read_customer_types(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)
):
    customer_types = get_customer_types(db, skip=skip, limit=limit)
    return customer_types

@router.put("/{customer_type_id}", response_model=CustomerType)
def update_existing_customer_type(
    customer_type_id: int,
    customer_type: CustomerTypeUpdate,
    db: Session = Depends(get_db_session),
):
    db_customer_type = update_customer_type(
        db, customer_type_id=customer_type_id, customer_type=customer_type
    )
    if db_customer_type is None:
        raise HTTPException(status_code=404, detail="CustomerType not found")
    return db_customer_type

@router.delete("/{customer_type_id}", response_model=CustomerType)
def delete_existing_customer_type(
    customer_type_id: int, db: Session = Depends(get_db_session)
):
    db_customer_type = delete_customer_type(db, customer_type_id=customer_type_id)
    if db_customer_type is None:
        raise HTTPException(status_code=404, detail="CustomerType not found")
    return db_customer_type
