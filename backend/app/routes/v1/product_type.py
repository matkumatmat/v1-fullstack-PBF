from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db_session
from app.schemas.product_type import ProductType, ProductTypeCreate, ProductTypeUpdate
from app.services.product_type import (
    create_product_type,
    delete_product_type,
    get_product_type,
    get_product_types,
    update_product_type,
)

router = APIRouter()

@router.post("/", response_model=ProductType)
def create_new_product_type(
    product_type: ProductTypeCreate, db: Session = Depends(get_db_session)
):
    return create_product_type(db=db, product_type=product_type)

@router.get("/{product_type_id}", response_model=ProductType)
def read_product_type(product_type_id: int, db: Session = Depends(get_db_session)):
    db_product_type = get_product_type(db, product_type_id=product_type_id)
    if db_product_type is None:
        raise HTTPException(status_code=404, detail="ProductType not found")
    return db_product_type

@router.get("/", response_model=List[ProductType])
def read_product_types(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)
):
    product_types = get_product_types(db, skip=skip, limit=limit)
    return product_types

@router.put("/{product_type_id}", response_model=ProductType)
def update_existing_product_type(
    product_type_id: int,
    product_type: ProductTypeUpdate,
    db: Session = Depends(get_db_session),
):
    db_product_type = update_product_type(
        db, product_type_id=product_type_id, product_type=product_type
    )
    if db_product_type is None:
        raise HTTPException(status_code=404, detail="ProductType not found")
    return db_product_type

@router.delete("/{product_type_id}", response_model=ProductType)
def delete_existing_product_type(
    product_type_id: int, db: Session = Depends(get_db_session)
):
    db_product_type = delete_product_type(db, product_type_id=product_type_id)
    if db_product_type is None:
        raise HTTPException(status_code=404, detail="ProductType not found")
    return db_product_type
