from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db_session
from app.schemas.allocation_type import AllocationType, AllocationTypeCreate, AllocationTypeUpdate
from app.services.allocation_type import (
    create_allocation_type,
    delete_allocation_type,
    get_allocation_type,
    get_allocation_types,
    update_allocation_type,
)

router = APIRouter()

@router.post("/", response_model=AllocationType)
def create_new_allocation_type(
    allocation_type: AllocationTypeCreate, db: Session = Depends(get_db_session)
):
    return create_allocation_type(db=db, allocation_type=allocation_type)

@router.get("/{allocation_type_id}", response_model=AllocationType)
def read_allocation_type(allocation_type_id: int, db: Session = Depends(get_db_session)):
    db_allocation_type = get_allocation_type(db, allocation_type_id=allocation_type_id)
    if db_allocation_type is None:
        raise HTTPException(status_code=404, detail="AllocationType not found")
    return db_allocation_type

@router.get("/", response_model=List[AllocationType])
def read_allocation_types(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)
):
    allocation_types = get_allocation_types(db, skip=skip, limit=limit)
    return allocation_types

@router.put("/{allocation_type_id}", response_model=AllocationType)
def update_existing_allocation_type(
    allocation_type_id: int,
    allocation_type: AllocationTypeUpdate,
    db: Session = Depends(get_db_session),
):
    db_allocation_type = update_allocation_type(
        db, allocation_type_id=allocation_type_id, allocation_type=allocation_type
    )
    if db_allocation_type is None:
        raise HTTPException(status_code=404, detail="AllocationType not found")
    return db_allocation_type

@router.delete("/{allocation_type_id}", response_model=AllocationType)
def delete_existing_allocation_type(
    allocation_type_id: int, db: Session = Depends(get_db_session)
):
    db_allocation_type = delete_allocation_type(db, allocation_type_id=allocation_type_id)
    if db_allocation_type is None:
        raise HTTPException(status_code=404, detail="AllocationType not found")
    return db_allocation_type
