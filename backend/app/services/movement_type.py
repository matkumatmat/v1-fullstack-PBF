from sqlalchemy.orm import Session
from app.models.type import MovementType
from app.schemas.movement_type import MovementTypeCreate, MovementTypeUpdate

def get_movement_type(db: Session, movement_type_id: int):
    return db.query(MovementType).filter(MovementType.id == movement_type_id).first()

def get_movement_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MovementType).offset(skip).limit(limit).all()

def create_movement_type(db: Session, movement_type: MovementTypeCreate):
    db_movement_type = MovementType(**movement_type.dict())
    db.add(db_movement_type)
    db.commit()
    db.refresh(db_movement_type)
    return db_movement_type

def update_movement_type(db: Session, movement_type_id: int, movement_type: MovementTypeUpdate):
    db_movement_type = db.query(MovementType).filter(MovementType.id == movement_type_id).first()
    if db_movement_type:
        update_data = movement_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_movement_type, key, value)
        db.commit()
        db.refresh(db_movement_type)
    return db_movement_type

def delete_movement_type(db: Session, movement_type_id: int):
    db_movement_type = db.query(MovementType).filter(MovementType.id == movement_type_id).first()
    if db_movement_type:
        db.delete(db_movement_type)
        db.commit()
    return db_movement_type
