from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db_session
from app.schemas.package_type import PackageType, PackageTypeCreate, PackageTypeUpdate
from app.services.package_type import (
    create_package_type,
    delete_package_type,
    get_package_type,
    get_package_types,
    update_package_type,
)

router = APIRouter()

@router.post("/", response_model=PackageType)
def create_new_package_type(
    package_type: PackageTypeCreate, db: Session = Depends(get_db_session)
):
    return create_package_type(db=db, package_type=package_type)

@router.get("/{package_type_id}", response_model=PackageType)
def read_package_type(package_type_id: int, db: Session = Depends(get_db_session)):
    db_package_type = get_package_type(db, package_type_id=package_type_id)
    if db_package_type is None:
        raise HTTPException(status_code=404, detail="PackageType not found")
    return db_package_type

@router.get("/", response_model=List[PackageType])
def read_package_types(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)
):
    package_types = get_package_types(db, skip=skip, limit=limit)
    return package_types

@router.put("/{package_type_id}", response_model=PackageType)
def update_existing_package_type(
    package_type_id: int,
    package_type: PackageTypeUpdate,
    db: Session = Depends(get_db_session),
):
    db_package_type = update_package_type(
        db, package_type_id=package_type_id, package_type=package_type
    )
    if db_package_type is None:
        raise HTTPException(status_code=404, detail="PackageType not found")
    return db_package_type

@router.delete("/{package_type_id}", response_model=PackageType)
def delete_existing_package_type(
    package_type_id: int, db: Session = Depends(get_db_session)
):
    db_package_type = delete_package_type(db, package_type_id=package_type_id)
    if db_package_type is None:
        raise HTTPException(status_code=404, detail="PackageType not found")
    return db_package_type
