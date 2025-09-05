from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db_session
from app.schemas.packaging_box_type import PackagingBoxType, PackagingBoxTypeCreate, PackagingBoxTypeUpdate
import app.services.packaging_box_type as packaging_box_type_service

router = APIRouter()

@router.post("/", response_model=PackagingBoxType)
async def create_packaging_box_type(
    packaging_box_type: PackagingBoxTypeCreate, db: AsyncSession = Depends(get_db_session)
):
    return await packaging_box_type_service.create_packaging_box_type(db=db, packaging_box_type=packaging_box_type)

@router.get("/", response_model=List[PackagingBoxType])
async def read_packaging_box_types(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)
):
    packaging_box_types = await packaging_box_type_service.get_packaging_box_types(db, skip=skip, limit=limit)
    return packaging_box_types

@router.get("/{packaging_box_type_id}", response_model=PackagingBoxType)
async def read_packaging_box_type(packaging_box_type_id: int, db: AsyncSession = Depends(get_db_session)):
    db_packaging_box_type = await packaging_box_type_service.get_packaging_box_type(db, packaging_box_type_id=packaging_box_type_id)
    if db_packaging_box_type is None:
        raise HTTPException(status_code=404, detail="PackagingBoxType not found")
    return db_packaging_box_type

@router.put("/{packaging_box_type_id}", response_model=PackagingBoxType)
async def update_packaging_box_type(
    packaging_box_type_id: int,
    packaging_box_type: PackagingBoxTypeUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    db_packaging_box_type = await packaging_box_type_service.update_packaging_box_type(
        db, packaging_box_type_id=packaging_box_type_id, packaging_box_type=packaging_box_type
    )
    if db_packaging_box_type is None:
        raise HTTPException(status_code=404, detail="PackagingBoxType not found")
    return db_packaging_box_type

@router.delete("/{packaging_box_type_id}", response_model=PackagingBoxType)
async def delete_packaging_box_type(
    packaging_box_type_id: int, db: AsyncSession = Depends(get_db_session)
):
    db_packaging_box_type = await packaging_box_type_service.delete_packaging_box_type(db, packaging_box_type_id=packaging_box_type_id)
    if db_packaging_box_type is None:
        raise HTTPException(status_code=404, detail="PackagingBoxType not found")
    return db_packaging_box_type