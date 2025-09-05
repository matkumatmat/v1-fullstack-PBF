from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.packaging_box_type import PackagingBoxType, PackagingBoxTypeCreate, PackagingBoxTypeUpdate
from app.services.packaging_box_type import (
    create_packaging_box_type,
    delete_packaging_box_type,
    get_packaging_box_type,
    get_packaging_box_types,
    update_packaging_box_type,
)

router = APIRouter()

@router.post("/", response_model=PackagingBoxType)
def create_new_packaging_box_type(
    packaging_box_type: PackagingBoxTypeCreate, db: Session = Depends(get_db)
):
    return create_packaging_box_type(db=db, packaging_box_type=packaging_box_type)

@router.get("/{packaging_box_type_id}", response_model=PackagingBoxType)
def read_packaging_box_type(packaging_box_type_id: int, db: Session = Depends(get_db)):
    db_packaging_box_type = get_packaging_box_type(db, packaging_box_type_id=packaging_box_type_id)
    if db_packaging_box_type is None:
        raise HTTPException(status_code=404, detail="PackagingBoxType not found")
    return db_packaging_box_type

@router.get("/", response_model=List[PackagingBoxType])
def read_packaging_box_types(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    packaging_box_types = get_packaging_box_types(db, skip=skip, limit=limit)
    return packaging_box_types

@router.put("/{packaging_box_type_id}", response_model=PackagingBoxType)
def update_existing_packaging_box_type(
    packaging_box_type_id: int,
    packaging_box_type: PackagingBoxTypeUpdate,
    db: Session = Depends(get_db),
):
    db_packaging_box_type = update_packaging_box_type(
        db, packaging_box_type_id=packaging_box_type_id, packaging_box_type=packaging_box_type
    )
    if db_packaging_box_type is None:
        raise HTTPException(status_code=404, detail="PackagingBoxType not found")
    return db_packaging_box_type

@router.delete("/{packaging_box_type_id}", response_model=PackagingBoxType)
def delete_existing_packaging_box_type(
    packaging_box_type_id: int, db: Session = Depends(get_db)
):
    db_packaging_box_type = delete_packaging_box_type(db, packaging_box_type_id=packaging_box_type_id)
    if db_packaging_box_type is None:
        raise HTTPException(status_code=404, detail="PackagingBoxType not found")
    return db_packaging_box_type
