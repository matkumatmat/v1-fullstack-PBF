from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db_session
from app.schemas.temperature_type import TemperatureType, TemperatureTypeCreate, TemperatureTypeUpdate
import app.services.temperature_type as temperature_type_service

router = APIRouter()

@router.post("/", response_model=TemperatureType)
async def create_temperature_type(
    temperature_type: TemperatureTypeCreate, db: AsyncSession = Depends(get_db_session)
):
    return await temperature_type_service.create_temperature_type(db=db, temperature_type=temperature_type)

@router.get("/", response_model=List[TemperatureType])
async def read_temperature_types(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)
):
    temperature_types = await temperature_type_service.get_temperature_types(db, skip=skip, limit=limit)
    return temperature_types

@router.get("/{temperature_type_id}", response_model=TemperatureType)
async def read_temperature_type(temperature_type_id: int, db: AsyncSession = Depends(get_db_session)):
    db_temperature_type = await temperature_type_service.get_temperature_type(db, temperature_type_id=temperature_type_id)
    if db_temperature_type is None:
        raise HTTPException(status_code=404, detail="TemperatureType not found")
    return db_temperature_type

@router.put("/{temperature_type_id}", response_model=TemperatureType)
async def update_temperature_type(
    temperature_type_id: int,
    temperature_type: TemperatureTypeUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    db_temperature_type = await temperature_type_service.update_temperature_type(
        db, temperature_type_id=temperature_type_id, temperature_type=temperature_type
    )
    if db_temperature_type is None:
        raise HTTPException(status_code=404, detail="TemperatureType not found")
    return db_temperature_type

@router.delete("/{temperature_type_id}", response_model=TemperatureType)
async def delete_temperature_type(
    temperature_type_id: int, db: AsyncSession = Depends(get_db_session)
):
    db_temperature_type = await temperature_type_service.delete_temperature_type(db, temperature_type_id=temperature_type_id)
    if db_temperature_type is None:
        raise HTTPException(status_code=404, detail="TemperatureType not found")
    return db_temperature_type