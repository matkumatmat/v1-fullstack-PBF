from sqlalchemy.orm import Session
from app.models.type import PackagingBoxType
from app.schemas.packaging_box_type import PackagingBoxTypeCreate, PackagingBoxTypeUpdate

def get_packaging_box_type(db: Session, packaging_box_type_id: int):
    return db.query(PackagingBoxType).filter(PackagingBoxType.id == packaging_box_type_id).first()

def get_packaging_box_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PackagingBoxType).offset(skip).limit(limit).all()

def create_packaging_box_type(db: Session, packaging_box_type: PackagingBoxTypeCreate):
    db_packaging_box_type = PackagingBoxType(**packaging_box_type.dict())
    db.add(db_packaging_box_type)
    db.commit()
    db.refresh(db_packaging_box_type)
    return db_packaging_box_type

def update_packaging_box_type(db: Session, packaging_box_type_id: int, packaging_box_type: PackagingBoxTypeUpdate):
    db_packaging_box_type = db.query(PackagingBoxType).filter(PackagingBoxType.id == packaging_box_type_id).first()
    if db_packaging_box_type:
        update_data = packaging_box_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_packaging_box_type, key, value)
        db.commit()
        db.refresh(db_packaging_box_type)
    return db_packaging_box_type

def delete_packaging_box_type(db: Session, packaging_box_type_id: int):
    db_packaging_box_type = db.query(PackagingBoxType).filter(PackagingBoxType.id == packaging_box_type_id).first()
    if db_packaging_box_type:
        db.delete(db_packaging_box_type)
        db.commit()
    return db_packaging_box_type
