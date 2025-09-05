from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db_session
from app.schemas.priority_level import PriorityLevel, PriorityLevelCreate, PriorityLevelUpdate
import app.services.priority_level as priority_level_service

router = APIRouter()

@router.post("/", response_model=PriorityLevel)
async def create_priority_level(
    priority_level: PriorityLevelCreate, db: AsyncSession = Depends(get_db_session)
):
    return await priority_level_service.create_priority_level(db=db, priority_level=priority_level)

@router.get("/", response_model=List[PriorityLevel])
async def read_priority_levels(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)
):
    priority_levels = await priority_level_service.get_priority_levels(db, skip=skip, limit=limit)
    return priority_levels

@router.get("/{priority_level_id}", response_model=PriorityLevel)
async def read_priority_level(priority_level_id: int, db: AsyncSession = Depends(get_db_session)):
    db_priority_level = await priority_level_service.get_priority_level(db, priority_level_id=priority_level_id)
    if db_priority_level is None:
        raise HTTPException(status_code=404, detail="PriorityLevel not found")
    return db_priority_level

@router.put("/{priority_level_id}", response_model=PriorityLevel)
async def update_priority_level(
    priority_level_id: int,
    priority_level: PriorityLevelUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    db_priority_level = await priority_level_service.update_priority_level(
        db, priority_level_id=priority_level_id, priority_level=priority_level
    )
    if db_priority_level is None:
        raise HTTPException(status_code=404, detail="PriorityLevel not found")
    return db_priority_level

@router.delete("/{priority_level_id}", response_model=PriorityLevel)
async def delete_priority_level(
    priority_level_id: int, db: AsyncSession = Depends(get_db_session)
):
    db_priority_level = await priority_level_service.delete_priority_level(db, priority_level_id=priority_level_id)
    if db_priority_level is None:
        raise HTTPException(status_code=404, detail="PriorityLevel not found")
    return db_priority_level