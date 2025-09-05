from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db_session
from app.schemas.movement_type import MovementType, MovementTypeCreate, MovementTypeUpdate
import app.services.movement_type as movement_type_service

router = APIRouter()

@router.post("/", response_model=MovementType)
async def create_movement_type(
    movement_type: MovementTypeCreate, db: AsyncSession = Depends(get_db_session)
):
    return await movement_type_service.create_movement_type(db=db, movement_type=movement_type)

@router.get("/", response_model=List[MovementType])
async def read_movement_types(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)
):
    movement_types = await movement_type_service.get_movement_types(db, skip=skip, limit=limit)
    return movement_types

@router.get("/{movement_type_id}", response_model=MovementType)
async def read_movement_type(movement_type_id: int, db: AsyncSession = Depends(get_db_session)):
    db_movement_type = await movement_type_service.get_movement_type(db, movement_type_id=movement_type_id)
    if db_movement_type is None:
        raise HTTPException(status_code=404, detail="MovementType not found")
    return db_movement_type

@router.put("/{movement_type_id}", response_model=MovementType)
async def update_movement_type(
    movement_type_id: int,
    movement_type: MovementTypeUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    db_movement_type = await movement_type_service.update_movement_type(
        db, movement_type_id=movement_type_id, movement_type=movement_type
    )
    if db_movement_type is None:
        raise HTTPException(status_code=404, detail="MovementType not found")
    return db_movement_type

@router.delete("/{movement_type_id}", response_model=MovementType)
async def delete_movement_type(
    movement_type_id: int, db: AsyncSession = Depends(get_db_session)
):
    db_movement_type = await movement_type_service.delete_movement_type(db, movement_type_id=movement_type_id)
    if db_movement_type is None:
        raise HTTPException(status_code=404, detail="MovementType not found")
    return db_movement_type