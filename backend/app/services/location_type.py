from sqlalchemy.orm import Session
from app.models.type import LocationType
from app.schemas.location_type import LocationTypeCreate, LocationTypeUpdate

def get_location_type(db: Session, location_type_id: int):
    return db.query(LocationType).filter(LocationType.id == location_type_id).first()

def get_location_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(LocationType).offset(skip).limit(limit).all()

def create_location_type(db: Session, location_type: LocationTypeCreate):
    db_location_type = LocationType(**location_type.dict())
    db.add(db_location_type)
    db.commit()
    db.refresh(db_location_type)
    return db_location_type

def update_location_type(db: Session, location_type_id: int, location_type: LocationTypeUpdate):
    db_location_type = db.query(LocationType).filter(LocationType.id == location_type_id).first()
    if db_location_type:
        update_data = location_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_location_type, key, value)
        db.commit()
        db.refresh(db_location_type)
    return db_location_type

def delete_location_type(db: Session, location_type_id: int):
    db_location_type = db.query(LocationType).filter(LocationType.id == location_type_id).first()
    if db_location_type:
        db.delete(db_location_type)
        db.commit()
    return db_location_type
