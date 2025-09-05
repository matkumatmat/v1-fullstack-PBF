from sqlalchemy.orm import Session
from app.models.type import PriorityLevel
from app.schemas.priority_level import PriorityLevelCreate, PriorityLevelUpdate

def get_priority_level(db: Session, priority_level_id: int):
    return db.query(PriorityLevel).filter(PriorityLevel.id == priority_level_id).first()

def get_priority_levels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PriorityLevel).offset(skip).limit(limit).all()

def create_priority_level(db: Session, priority_level: PriorityLevelCreate):
    db_priority_level = PriorityLevel(**priority_level.dict())
    db.add(db_priority_level)
    db.commit()
    db.refresh(db_priority_level)
    return db_priority_level

def update_priority_level(db: Session, priority_level_id: int, priority_level: PriorityLevelUpdate):
    db_priority_level = db.query(PriorityLevel).filter(PriorityLevel.id == priority_level_id).first()
    if db_priority_level:
        update_data = priority_level.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_priority_level, key, value)
        db.commit()
        db.refresh(db_priority_level)
    return db_priority_level

def delete_priority_level(db: Session, priority_level_id: int):
    db_priority_level = db.query(PriorityLevel).filter(PriorityLevel.id == priority_level_id).first()
    if db_priority_level:
        db.delete(db_priority_level)
        db.commit()
    return db_priority_level
