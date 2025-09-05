from sqlalchemy.orm import Session
from app.models.type import SectorType
from app.schemas.sector_type import SectorTypeCreate, SectorTypeUpdate

def get_sector_type(db: Session, sector_type_id: int):
    return db.query(SectorType).filter(SectorType.id == sector_type_id).first()

def get_sector_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SectorType).offset(skip).limit(limit).all()

def create_sector_type(db: Session, sector_type: SectorTypeCreate):
    db_sector_type = SectorType(**sector_type.dict())
    db.add(db_sector_type)
    db.commit()
    db.refresh(db_sector_type)
    return db_sector_type

def update_sector_type(db: Session, sector_type_id: int, sector_type: SectorTypeUpdate):
    db_sector_type = db.query(SectorType).filter(SectorType.id == sector_type_id).first()
    if db_sector_type:
        update_data = sector_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_sector_type, key, value)
        db.commit()
        db.refresh(db_sector_type)
    return db_sector_type

def delete_sector_type(db: Session, sector_type_id: int):
    db_sector_type = db.query(SectorType).filter(SectorType.id == sector_type_id).first()
    if db_sector_type:
        db.delete(db_sector_type)
        db.commit()
    return db_sector_type
