from sqlalchemy.orm import Session
from app.models.type import CustomerType
from app.schemas.customer_type import CustomerTypeCreate, CustomerTypeUpdate

def get_customer_type(db: Session, customer_type_id: int):
    return db.query(CustomerType).filter(CustomerType.id == customer_type_id).first()

def get_customer_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CustomerType).offset(skip).limit(limit).all()

def create_customer_type(db: Session, customer_type: CustomerTypeCreate):
    db_customer_type = CustomerType(**customer_type.dict())
    db.add(db_customer_type)
    db.commit()
    db.refresh(db_customer_type)
    return db_customer_type

def update_customer_type(db: Session, customer_type_id: int, customer_type: CustomerTypeUpdate):
    db_customer_type = db.query(CustomerType).filter(CustomerType.id == customer_type_id).first()
    if db_customer_type:
        update_data = customer_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_customer_type, key, value)
        db.commit()
        db.refresh(db_customer_type)
    return db_customer_type

def delete_customer_type(db: Session, customer_type_id: int):
    db_customer_type = db.query(CustomerType).filter(CustomerType.id == customer_type_id).first()
    if db_customer_type:
        db.delete(db_customer_type)
        db.commit()
    return db_customer_type
