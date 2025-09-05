from sqlalchemy.orm import Session
from app.models.type import StatusType
from app.schemas.status_type import StatusTypeCreate, StatusTypeUpdate

def get_status_type(db: Session, status_type_id: int):
    return db.query(StatusType).filter(StatusType.id == status_type_id).first()

def get_status_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(StatusType).offset(skip).limit(limit).all()

def create_status_type(db: Session, status_type: StatusTypeCreate):
    db_status_type = StatusType(**status_type.dict())
    db.add(db_status_type)
    db.commit()
    db.refresh(db_status_type)
    return db_status_type

def update_status_type(db: Session, status_type_id: int, status_type: StatusTypeUpdate):
    db_status_type = db.query(StatusType).filter(StatusType.id == status_type_id).first()
    if db_status_type:
        update_data = status_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_status_type, key, value)
        db.commit()
        db.refresh(db_status_type)
    return db_status_type

def delete_status_type(db: Session, status_type_id: int):
    db_status_type = db.query(StatusType).filter(StatusType.id == status_type_id).first()
    if db_status_type:
        db.delete(db_status_type)
        db.commit()
    return db_status_type
