from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.sector_type import SectorType, SectorTypeCreate, SectorTypeUpdate
from app.services.sector_type import (
    create_sector_type,
    delete_sector_type,
    get_sector_type,
    get_sector_types,
    update_sector_type,
)

router = APIRouter()

@router.post("/", response_model=SectorType)
def create_new_sector_type(
    sector_type: SectorTypeCreate, db: Session = Depends(get_db)
):
    return create_sector_type(db=db, sector_type=sector_type)

@router.get("/{sector_type_id}", response_model=SectorType)
def read_sector_type(sector_type_id: int, db: Session = Depends(get_db)):
    db_sector_type = get_sector_type(db, sector_type_id=sector_type_id)
    if db_sector_type is None:
        raise HTTPException(status_code=404, detail="SectorType not found")
    return db_sector_type

@router.get("/", response_model=List[SectorType])
def read_sector_types(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    sector_types = get_sector_types(db, skip=skip, limit=limit)
    return sector_types

@router.put("/{sector_type_id}", response_model=SectorType)
def update_existing_sector_type(
    sector_type_id: int,
    sector_type: SectorTypeUpdate,
    db: Session = Depends(get_db),
):
    db_sector_type = update_sector_type(
        db, sector_type_id=sector_type_id, sector_type=sector_type
    )
    if db_sector_type is None:
        raise HTTPException(status_code=404, detail="SectorType not found")
    return db_sector_type

@router.delete("/{sector_type_id}", response_model=SectorType)
def delete_existing_sector_type(
    sector_type_id: int, db: Session = Depends(get_db)
):
    db_sector_type = delete_sector_type(db, sector_type_id=sector_type_id)
    if db_sector_type is None:
        raise HTTPException(status_code=404, detail="SectorType not found")
    return db_sector_type
