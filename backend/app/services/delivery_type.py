from sqlalchemy.orm import Session
from app.models.type import DeliveryType
from app.schemas.delivery_type import DeliveryTypeCreate, DeliveryTypeUpdate

def get_delivery_type(db: Session, delivery_type_id: int):
    return db.query(DeliveryType).filter(DeliveryType.id == delivery_type_id).first()

def get_delivery_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DeliveryType).offset(skip).limit(limit).all()

def create_delivery_type(db: Session, delivery_type: DeliveryTypeCreate):
    db_delivery_type = DeliveryType(**delivery_type.dict())
    db.add(db_delivery_type)
    db.commit()
    db.refresh(db_delivery_type)
    return db_delivery_type

def update_delivery_type(db: Session, delivery_type_id: int, delivery_type: DeliveryTypeUpdate):
    db_delivery_type = db.query(DeliveryType).filter(DeliveryType.id == delivery_type_id).first()
    if db_delivery_type:
        update_data = delivery_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_delivery_type, key, value)
        db.commit()
        db.refresh(db_delivery_type)
    return db_delivery_type

def delete_delivery_type(db: Session, delivery_type_id: int):
    db_delivery_type = db.query(DeliveryType).filter(DeliveryType.id == delivery_type_id).first()
    if db_delivery_type:
        db.delete(db_delivery_type)
        db.commit()
    return db_delivery_type
