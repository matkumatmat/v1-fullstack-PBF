from sqlalchemy.orm import Session
from app.models.type import PackageType
from app.schemas.package_type import PackageTypeCreate, PackageTypeUpdate

def get_package_type(db: Session, package_type_id: int):
    return db.query(PackageType).filter(PackageType.id == package_type_id).first()

def get_package_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PackageType).offset(skip).limit(limit).all()

def create_package_type(db: Session, package_type: PackageTypeCreate):
    db_package_type = PackageType(**package_type.dict())
    db.add(db_package_type)
    db.commit()
    db.refresh(db_package_type)
    return db_package_type

def update_package_type(db: Session, package_type_id: int, package_type: PackageTypeUpdate):
    db_package_type = db.query(PackageType).filter(PackageType.id == package_type_id).first()
    if db_package_type:
        update_data = package_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_package_type, key, value)
        db.commit()
        db.refresh(db_package_type)
    return db_package_type

def delete_package_type(db: Session, package_type_id: int):
    db_package_type = db.query(PackageType).filter(PackageType.id == package_type_id).first()
    if db_package_type:
        db.delete(db_package_type)
        db.commit()
    return db_package_type
