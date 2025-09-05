from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.movement_type import MovementType, MovementTypeCreate, MovementTypeUpdate
from app.services.movement_type import (
    create_movement_type,
    delete_movement_type,
    get_movement_type,
    get_movement_types,
    update_movement_type,
)

router = APIRouter()

@router.post("/", response_model=MovementType)
def create_new_movement_type(
    movement_type: MovementTypeCreate, db: Session = Depends(get_db)
):
    return create_movement_type(db=db, movement_type=movement_type)

@router.get("/{movement_type_id}", response_model=MovementType)
def read_movement_type(movement_type_id: int, db: Session = Depends(get_db)):
    db_movement_type = get_movement_type(db, movement_type_id=movement_type_id)
    if db_movement_type is None:
        raise HTTPException(status_code=404, detail="MovementType not found")
    return db_movement_type

@router.get("/", response_model=List[MovementType])
def read_movement_types(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    movement_types = get_movement_types(db, skip=skip, limit=limit)
    return movement_types

@router.put("/{movement_type_id}", response_model=MovementType)
def update_existing_movement_type(
    movement_type_id: int,
    movement_type: MovementTypeUpdate,
    db: Session = Depends(get_db),
):
    db_movement_type = update_movement_type(
        db, movement_type_id=movement_type_id, movement_type=movement_type
    )
    if db_movement_type is None:
        raise HTTPException(status_code=404, detail="MovementType not found")
    return db_movement_type

@router.delete("/{movement_type_id}", response_model=MovementType)
def delete_existing_movement_type(
    movement_type_id: int, db: Session = Depends(get_db)
):
    db_movement_type = delete_movement_type(db, movement_type_id=movement_type_id)
    if db_movement_type is None:
        raise HTTPException(status_code=404, detail="MovementType not found")
    return db_movement_type
