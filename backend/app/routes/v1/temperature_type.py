from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.temperature_type import TemperatureType, TemperatureTypeCreate, TemperatureTypeUpdate
from app.services.temperature_type import (
    create_temperature_type,
    delete_temperature_type,
    get_temperature_type,
    get_temperature_types,
    update_temperature_type,
)

router = APIRouter()

@router.post("/", response_model=TemperatureType)
def create_new_temperature_type(
    temperature_type: TemperatureTypeCreate, db: Session = Depends(get_db)
):
    return create_temperature_type(db=db, temperature_type=temperature_type)

@router.get("/{temperature_type_id}", response_model=TemperatureType)
def read_temperature_type(temperature_type_id: int, db: Session = Depends(get_db)):
    db_temperature_type = get_temperature_type(db, temperature_type_id=temperature_type_id)
    if db_temperature_type is None:
        raise HTTPException(status_code=404, detail="TemperatureType not found")
    return db_temperature_type

@router.get("/", response_model=List[TemperatureType])
def read_temperature_types(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    temperature_types = get_temperature_types(db, skip=skip, limit=limit)
    return temperature_types

@router.put("/{temperature_type_id}", response_model=TemperatureType)
def update_existing_temperature_type(
    temperature_type_id: int,
    temperature_type: TemperatureTypeUpdate,
    db: Session = Depends(get_db),
):
    db_temperature_type = update_temperature_type(
        db, temperature_type_id=temperature_type_id, temperature_type=temperature_type
    )
    if db_temperature_type is None:
        raise HTTPException(status_code=404, detail="TemperatureType not found")
    return db_temperature_type

@router.delete("/{temperature_type_id}", response_model=TemperatureType)
def delete_existing_temperature_type(
    temperature_type_id: int, db: Session = Depends(get_db)
):
    db_temperature_type = delete_temperature_type(db, temperature_type_id=temperature_type_id)
    if db_temperature_type is None:
        raise HTTPException(status_code=404, detail="TemperatureType not found")
    return db_temperature_type
