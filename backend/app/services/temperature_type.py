from sqlalchemy.orm import Session
from app.models.type import TemperatureType
from app.schemas.temperature_type import TemperatureTypeCreate, TemperatureTypeUpdate

def get_temperature_type(db: Session, temperature_type_id: int):
    return db.query(TemperatureType).filter(TemperatureType.id == temperature_type_id).first()

def get_temperature_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TemperatureType).offset(skip).limit(limit).all()

def create_temperature_type(db: Session, temperature_type: TemperatureTypeCreate):
    db_temperature_type = TemperatureType(**temperature_type.dict())
    db.add(db_temperature_type)
    db.commit()
    db.refresh(db_temperature_type)
    return db_temperature_type

def update_temperature_type(db: Session, temperature_type_id: int, temperature_type: TemperatureTypeUpdate):
    db_temperature_type = db.query(TemperatureType).filter(TemperatureType.id == temperature_type_id).first()
    if db_temperature_type:
        update_data = temperature_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_temperature_type, key, value)
        db.commit()
        db.refresh(db_temperature_type)
    return db_temperature_type

def delete_temperature_type(db: Session, temperature_type_id: int):
    db_temperature_type = db.query(TemperatureType).filter(TemperatureType.id == temperature_type_id).first()
    if db_temperature_type:
        db.delete(db_temperature_type)
        db.commit()
    return db_temperature_type
