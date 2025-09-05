from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db_session
from app.schemas.package_type import PackageType, PackageTypeCreate, PackageTypeUpdate
import app.services.package_type as package_type_service

router = APIRouter()

@router.post("/", response_model=PackageType)
async def create_package_type(
    package_type: PackageTypeCreate, db: AsyncSession = Depends(get_db_session)
):
    return await package_type_service.create_package_type(db=db, package_type=package_type)

@router.get("/", response_model=List[PackageType])
async def read_package_types(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)
):
    package_types = await package_type_service.get_package_types(db, skip=skip, limit=limit)
    return package_types

@router.get("/{package_type_id}", response_model=PackageType)
async def read_package_type(package_type_id: int, db: AsyncSession = Depends(get_db_session)):
    db_package_type = await package_type_service.get_package_type(db, package_type_id=package_type_id)
    if db_package_type is None:
        raise HTTPException(status_code=404, detail="PackageType not found")
    return db_package_type

@router.put("/{package_type_id}", response_model=PackageType)
async def update_package_type(
    package_type_id: int,
    package_type: PackageTypeUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    db_package_type = await package_type_service.update_package_type(
        db, package_type_id=package_type_id, package_type=package_type
    )
    if db_package_type is None:
        raise HTTPException(status_code=404, detail="PackageType not found")
    return db_package_type

@router.delete("/{package_type_id}", response_model=PackageType)
async def delete_package_type(
    package_type_id: int, db: AsyncSession = Depends(get_db_session)
):
    db_package_type = await package_type_service.delete_package_type(db, package_type_id=package_type_id)
    if db_package_type is None:
        raise HTTPException(status_code=404, detail="PackageType not found")
    return db_package_type