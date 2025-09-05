from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db_session
from app.schemas.location_type import LocationType, LocationTypeCreate, LocationTypeUpdate
from app.services.location_type import (
    create_location_type,
    delete_location_type,
    get_location_type,
    get_location_types,
    update_location_type,
)

router = APIRouter()

@router.post("/", response_model=LocationType)
def create_new_location_type(
    location_type: LocationTypeCreate, db: Session = Depends(get_db_session)
):
    return create_location_type(db=db, location_type=location_type)

@router.get("/{location_type_id}", response_model=LocationType)
def read_location_type(location_type_id: int, db: Session = Depends(get_db_session)):
    db_location_type = get_location_type(db, location_type_id=location_type_id)
    if db_location_type is None:
        raise HTTPException(status_code=404, detail="LocationType not found")
    return db_location_type

@router.get("/", response_model=List[LocationType])
def read_location_types(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)
):
    location_types = get_location_types(db, skip=skip, limit=limit)
    return location_types

@router.put("/{location_type_id}", response_model=LocationType)
def update_existing_location_type(
    location_type_id: int,
    location_type: LocationTypeUpdate,
    db: Session = Depends(get_db_session),
):
    db_location_type = update_location_type(
        db, location_type_id=location_type_id, location_type=location_type
    )
    if db_location_type is None:
        raise HTTPException(status_code=404, detail="LocationType not found")
    return db_location_type

@router.delete("/{location_type_id}", response_model=LocationType)
def delete_existing_location_type(
    location_type_id: int, db: Session = Depends(get_db_session)
):
    db_location_type = delete_location_type(db, location_type_id=location_type_id)
    if db_location_type is None:
        raise HTTPException(status_code=404, detail="LocationType not found")
    return db_location_type
