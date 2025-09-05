from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db_session
from app.schemas.allocation_type import AllocationType, AllocationTypeCreate, AllocationTypeUpdate
import app.services.allocation_type as allocation_type_service

router = APIRouter()

@router.post("/", response_model=AllocationType)
async def create_allocation_type(
    allocation_type: AllocationTypeCreate, db: AsyncSession = Depends(get_db_session)
):
    return await allocation_type_service.create_allocation_type(db=db, allocation_type=allocation_type)

@router.get("/", response_model=List[AllocationType])
async def read_allocation_types(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)
):
    allocation_types = await allocation_type_service.get_allocation_types(db, skip=skip, limit=limit)
    return allocation_types

@router.get("/{allocation_type_id}", response_model=AllocationType)
async def read_allocation_type(allocation_type_id: int, db: AsyncSession = Depends(get_db_session)):
    db_allocation_type = await allocation_type_service.get_allocation_type(db, allocation_type_id=allocation_type_id)
    if db_allocation_type is None:
        raise HTTPException(status_code=404, detail="AllocationType not found")
    return db_allocation_type

@router.put("/{allocation_type_id}", response_model=AllocationType)
async def update_allocation_type(
    allocation_type_id: int,
    allocation_type: AllocationTypeUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    db_allocation_type = await allocation_type_service.update_allocation_type(
        db, allocation_type_id=allocation_type_id, allocation_type=allocation_type
    )
    if db_allocation_type is None:
        raise HTTPException(status_code=404, detail="AllocationType not found")
    return db_allocation_type

@router.delete("/{allocation_type_id}", response_model=AllocationType)
async def delete_allocation_type(
    allocation_type_id: int, db: AsyncSession = Depends(get_db_session)
):
    db_allocation_type = await allocation_type_service.delete_allocation_type(db, allocation_type_id=allocation_type_id)
    if db_allocation_type is None:
        raise HTTPException(status_code=404, detail="AllocationType not found")
    return db_allocation_type