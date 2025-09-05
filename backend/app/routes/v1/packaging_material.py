from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db_session
from app.schemas.packaging_material import PackagingMaterial, PackagingMaterialCreate, PackagingMaterialUpdate
import app.services.packaging_material as packaging_material_service

router = APIRouter()

@router.post("/", response_model=PackagingMaterial)
async def create_packaging_material(
    packaging_material: PackagingMaterialCreate, db: AsyncSession = Depends(get_db_session)
):
    return await packaging_material_service.create_packaging_material(db=db, packaging_material=packaging_material)

@router.get("/", response_model=List[PackagingMaterial])
async def read_packaging_materials(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)
):
    packaging_materials = await packaging_material_service.get_packaging_materials(db, skip=skip, limit=limit)
    return packaging_materials

@router.get("/{packaging_material_id}", response_model=PackagingMaterial)
async def read_packaging_material(packaging_material_id: int, db: AsyncSession = Depends(get_db_session)):
    db_packaging_material = await packaging_material_service.get_packaging_material(db, packaging_material_id=packaging_material_id)
    if db_packaging_material is None:
        raise HTTPException(status_code=404, detail="PackagingMaterial not found")
    return db_packaging_material

@router.put("/{packaging_material_id}", response_model=PackagingMaterial)
async def update_packaging_material(
    packaging_material_id: int,
    packaging_material: PackagingMaterialUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    db_packaging_material = await packaging_material_service.update_packaging_material(
        db, packaging_material_id=packaging_material_id, packaging_material=packaging_material
    )
    if db_packaging_material is None:
        raise HTTPException(status_code=404, detail="PackagingMaterial not found")
    return db_packaging_material

@router.delete("/{packaging_material_id}", response_model=PackagingMaterial)
async def delete_packaging_material(
    packaging_material_id: int, db: AsyncSession = Depends(get_db_session)
):
    db_packaging_material = await packaging_material_service.delete_packaging_material(db, packaging_material_id=packaging_material_id)
    if db_packaging_material is None:
        raise HTTPException(status_code=404, detail="PackagingMaterial not found")
    return db_packaging_material