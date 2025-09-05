from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db_session
from app.schemas.location_type import LocationType, LocationTypeCreate, LocationTypeUpdate
import app.services.location_type as location_type_service

router = APIRouter()

@router.post("/", response_model=LocationType)
async def create_location_type(
    location_type: LocationTypeCreate, db: AsyncSession = Depends(get_db_session)
):
    return await location_type_service.create_location_type(db=db, location_type=location_type)

@router.get("/", response_model=List[LocationType])
async def read_location_types(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)
):
    location_types = await location_type_service.get_location_types(db, skip=skip, limit=limit)
    return location_types

@router.get("/{location_type_id}", response_model=LocationType)
async def read_location_type(location_type_id: int, db: AsyncSession = Depends(get_db_session)):
    db_location_type = await location_type_service.get_location_type(db, location_type_id=location_type_id)
    if db_location_type is None:
        raise HTTPException(status_code=404, detail="LocationType not found")
    return db_location_type

@router.put("/{location_type_id}", response_model=LocationType)
async def update_location_type(
    location_type_id: int,
    location_type: LocationTypeUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    db_location_type = await location_type_service.update_location_type(
        db, location_type_id=location_type_id, location_type=location_type
    )
    if db_location_type is None:
        raise HTTPException(status_code=404, detail="LocationType not found")
    return db_location_type

@router.delete("/{location_type_id}", response_model=LocationType)
async def delete_location_type(
    location_type_id: int, db: AsyncSession = Depends(get_db_session)
):
    db_location_type = await location_type_service.delete_location_type(db, location_type_id=location_type_id)
    if db_location_type is None:
        raise HTTPException(status_code=404, detail="LocationType not found")
    return db_location_type