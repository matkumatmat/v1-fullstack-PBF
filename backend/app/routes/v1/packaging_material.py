from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.packaging_material import PackagingMaterial, PackagingMaterialCreate, PackagingMaterialUpdate
from app.services.packaging_material import (
    create_packaging_material,
    delete_packaging_material,
    get_packaging_material,
    get_packaging_materials,
    update_packaging_material,
)

router = APIRouter()

@router.post("/", response_model=PackagingMaterial)
def create_new_packaging_material(
    packaging_material: PackagingMaterialCreate, db: Session = Depends(get_db)
):
    return create_packaging_material(db=db, packaging_material=packaging_material)

@router.get("/{packaging_material_id}", response_model=PackagingMaterial)
def read_packaging_material(packaging_material_id: int, db: Session = Depends(get_db)):
    db_packaging_material = get_packaging_material(db, packaging_material_id=packaging_material_id)
    if db_packaging_material is None:
        raise HTTPException(status_code=404, detail="PackagingMaterial not found")
    return db_packaging_material

@router.get("/", response_model=List[PackagingMaterial])
def read_packaging_materials(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    packaging_materials = get_packaging_materials(db, skip=skip, limit=limit)
    return packaging_materials

@router.put("/{packaging_material_id}", response_model=PackagingMaterial)
def update_existing_packaging_material(
    packaging_material_id: int,
    packaging_material: PackagingMaterialUpdate,
    db: Session = Depends(get_db),
):
    db_packaging_material = update_packaging_material(
        db, packaging_material_id=packaging_material_id, packaging_material=packaging_material
    )
    if db_packaging_material is None:
        raise HTTPException(status_code=404, detail="PackagingMaterial not found")
    return db_packaging_material

@router.delete("/{packaging_material_id}", response_model=PackagingMaterial)
def delete_existing_packaging_material(
    packaging_material_id: int, db: Session = Depends(get_db)
):
    db_packaging_material = delete_packaging_material(db, packaging_material_id=packaging_material_id)
    if db_packaging_material is None:
        raise HTTPException(status_code=404, detail="PackagingMaterial not found")
    return db_packaging_material
