from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.priority_level import PriorityLevel, PriorityLevelCreate, PriorityLevelUpdate
from app.services.priority_level import (
    create_priority_level,
    delete_priority_level,
    get_priority_level,
    get_priority_levels,
    update_priority_level,
)

router = APIRouter()

@router.post("/", response_model=PriorityLevel)
def create_new_priority_level(
    priority_level: PriorityLevelCreate, db: Session = Depends(get_db)
):
    return create_priority_level(db=db, priority_level=priority_level)

@router.get("/{priority_level_id}", response_model=PriorityLevel)
def read_priority_level(priority_level_id: int, db: Session = Depends(get_db)):
    db_priority_level = get_priority_level(db, priority_level_id=priority_level_id)
    if db_priority_level is None:
        raise HTTPException(status_code=404, detail="PriorityLevel not found")
    return db_priority_level

@router.get("/", response_model=List[PriorityLevel])
def read_priority_levels(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    priority_levels = get_priority_levels(db, skip=skip, limit=limit)
    return priority_levels

@router.put("/{priority_level_id}", response_model=PriorityLevel)
def update_existing_priority_level(
    priority_level_id: int,
    priority_level: PriorityLevelUpdate,
    db: Session = Depends(get_db),
):
    db_priority_level = update_priority_level(
        db, priority_level_id=priority_level_id, priority_level=priority_level
    )
    if db_priority_level is None:
        raise HTTPException(status_code=404, detail="PriorityLevel not found")
    return db_priority_level

@router.delete("/{priority_level_id}", response_model=PriorityLevel)
def delete_existing_priority_level(
    priority_level_id: int, db: Session = Depends(get_db)
):
    db_priority_level = delete_priority_level(db, priority_level_id=priority_level_id)
    if db_priority_level is None:
        raise HTTPException(status_code=404, detail="PriorityLevel not found")
    return db_priority_level
