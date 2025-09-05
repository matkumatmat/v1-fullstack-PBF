from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db_session
from app.schemas.sector_type import SectorType, SectorTypeCreate, SectorTypeUpdate
import app.services.sector_type as sector_type_service

router = APIRouter()

@router.post("/", response_model=SectorType)
async def create_sector_type(
    sector_type: SectorTypeCreate, db: AsyncSession = Depends(get_db_session)
):
    return await sector_type_service.create_sector_type(db=db, sector_type=sector_type)

@router.get("/", response_model=List[SectorType])
async def read_sector_types(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)
):
    sector_types = await sector_type_service.get_sector_types(db, skip=skip, limit=limit)
    return sector_types

@router.get("/{sector_type_id}", response_model=SectorType)
async def read_sector_type(sector_type_id: int, db: AsyncSession = Depends(get_db_session)):
    db_sector_type = await sector_type_service.get_sector_type(db, sector_type_id=sector_type_id)
    if db_sector_type is None:
        raise HTTPException(status_code=404, detail="SectorType not found")
    return db_sector_type

@router.put("/{sector_type_id}", response_model=SectorType)
async def update_sector_type(
    sector_type_id: int,
    sector_type: SectorTypeUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    db_sector_type = await sector_type_service.update_sector_type(
        db, sector_type_id=sector_type_id, sector_type=sector_type
    )
    if db_sector_type is None:
        raise HTTPException(status_code=404, detail="SectorType not found")
    return db_sector_type

@router.delete("/{sector_type_id}", response_model=SectorType)
async def delete_sector_type(
    sector_type_id: int, db: AsyncSession = Depends(get_db_session)
):
    db_sector_type = await sector_type_service.delete_sector_type(db, sector_type_id=sector_type_id)
    if db_sector_type is None:
        raise HTTPException(status_code=404, detail="SectorType not found")
    return db_sector_type