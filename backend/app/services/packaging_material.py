from sqlalchemy.orm import Session
from app.models.type import PackagingMaterial
from app.schemas.packaging_material import PackagingMaterialCreate, PackagingMaterialUpdate

def get_packaging_material(db: Session, packaging_material_id: int):
    return db.query(PackagingMaterial).filter(PackagingMaterial.id == packaging_material_id).first()

def get_packaging_materials(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PackagingMaterial).offset(skip).limit(limit).all()

def create_packaging_material(db: Session, packaging_material: PackagingMaterialCreate):
    db_packaging_material = PackagingMaterial(**packaging_material.dict())
    db.add(db_packaging_material)
    db.commit()
    db.refresh(db_packaging_material)
    return db_packaging_material

def update_packaging_material(db: Session, packaging_material_id: int, packaging_material: PackagingMaterialUpdate):
    db_packaging_material = db.query(PackagingMaterial).filter(PackagingMaterial.id == packaging_material_id).first()
    if db_packaging_material:
        update_data = packaging_material.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_packaging_material, key, value)
        db.commit()
        db.refresh(db_packaging_material)
    return db_packaging_material

def delete_packaging_material(db: Session, packaging_material_id: int):
    db_packaging_material = db.query(PackagingMaterial).filter(PackagingMaterial.id == packaging_material_id).first()
    if db_packaging_material:
        db.delete(db_packaging_material)
        db.commit()
    return db_packaging_material
