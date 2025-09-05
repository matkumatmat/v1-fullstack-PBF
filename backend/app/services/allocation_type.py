from sqlalchemy.orm import Session
from app.models.type import AllocationType
from app.schemas.allocation_type import AllocationTypeCreate, AllocationTypeUpdate

def get_allocation_type(db: Session, allocation_type_id: int):
    return db.query(AllocationType).filter(AllocationType.id == allocation_type_id).first()

def get_allocation_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AllocationType).offset(skip).limit(limit).all()

def create_allocation_type(db: Session, allocation_type: AllocationTypeCreate):
    db_allocation_type = AllocationType(**allocation_type.dict())
    db.add(db_allocation_type)
    db.commit()
    db.refresh(db_allocation_type)
    return db_allocation_type

def update_allocation_type(db: Session, allocation_type_id: int, allocation_type: AllocationTypeUpdate):
    db_allocation_type = db.query(AllocationType).filter(AllocationType.id == allocation_type_id).first()
    if db_allocation_type:
        update_data = allocation_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_allocation_type, key, value)
        db.commit()
        db.refresh(db_allocation_type)
    return db_allocation_type

def delete_allocation_type(db: Session, allocation_type_id: int):
    db_allocation_type = db.query(AllocationType).filter(AllocationType.id == allocation_type_id).first()
    if db_allocation_type:
        db.delete(db_allocation_type)
        db.commit()
    return db_allocation_type
