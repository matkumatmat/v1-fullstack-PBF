from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db_session
from app.schemas.status_type import StatusType, StatusTypeCreate, StatusTypeUpdate
import app.services.status_type as status_type_service

router = APIRouter()

@router.post("/", response_model=StatusType)
async def create_status_type(
    status_type: StatusTypeCreate, db: AsyncSession = Depends(get_db_session)
):
    return await status_type_service.create_status_type(db=db, status_type=status_type)

@router.get("/", response_model=List[StatusType])
async def read_status_types(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)
):
    status_types = await status_type_service.get_status_types(db, skip=skip, limit=limit)
    return status_types

@router.get("/{status_type_id}", response_model=StatusType)
async def read_status_type(status_type_id: int, db: AsyncSession = Depends(get_db_session)):
    db_status_type = await status_type_service.get_status_type(db, status_type_id=status_type_id)
    if db_status_type is None:
        raise HTTPException(status_code=404, detail="StatusType not found")
    return db_status_type

@router.put("/{status_type_id}", response_model=StatusType)
async def update_status_type(
    status_type_id: int,
    status_type: StatusTypeUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    db_status_type = await status_type_service.update_status_type(
        db, status_type_id=status_type_id, status_type=status_type
    )
    if db_status_type is None:
        raise HTTPException(status_code=404, detail="StatusType not found")
    return db_status_type

@router.delete("/{status_type_id}", response_model=StatusType)
async def delete_status_type(
    status_type_id: int, db: AsyncSession = Depends(get_db_session)
):
    db_status_type = await status_type_service.delete_status_type(db, status_type_id=status_type_id)
    if db_status_type is None:
        raise HTTPException(status_code=404, detail="StatusType not found")
    return db_status_type