from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.status_type import StatusType, StatusTypeCreate, StatusTypeUpdate
from app.services.status_type import (
    create_status_type,
    delete_status_type,
    get_status_type,
    get_status_types,
    update_status_type,
)

router = APIRouter()

@router.post("/", response_model=StatusType)
def create_new_status_type(
    status_type: StatusTypeCreate, db: Session = Depends(get_db)
):
    return create_status_type(db=db, status_type=status_type)

@router.get("/{status_type_id}", response_model=StatusType)
def read_status_type(status_type_id: int, db: Session = Depends(get_db)):
    db_status_type = get_status_type(db, status_type_id=status_type_id)
    if db_status_type is None:
        raise HTTPException(status_code=404, detail="StatusType not found")
    return db_status_type

@router.get("/", response_model=List[StatusType])
def read_status_types(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    status_types = get_status_types(db, skip=skip, limit=limit)
    return status_types

@router.put("/{status_type_id}", response_model=StatusType)
def update_existing_status_type(
    status_type_id: int,
    status_type: StatusTypeUpdate,
    db: Session = Depends(get_db),
):
    db_status_type = update_status_type(
        db, status_type_id=status_type_id, status_type=status_type
    )
    if db_status_type is None:
        raise HTTPException(status_code=404, detail="StatusType not found")
    return db_status_type

@router.delete("/{status_type_id}", response_model=StatusType)
def delete_existing_status_type(
    status_type_id: int, db: Session = Depends(get_db)
):
    db_status_type = delete_status_type(db, status_type_id=status_type_id)
    if db_status_type is None:
        raise HTTPException(status_code=404, detail="StatusType not found")
    return db_status_type
