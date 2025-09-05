from sqlalchemy.orm import Session
from app.models.type import ProductType
from app.schemas.product_type import ProductTypeCreate, ProductTypeUpdate

def get_product_type(db: Session, product_type_id: int):
    return db.query(ProductType).filter(ProductType.id == product_type_id).first()

def get_product_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProductType).offset(skip).limit(limit).all()

def create_product_type(db: Session, product_type: ProductTypeCreate):
    db_product_type = ProductType(**product_type.dict())
    db.add(db_product_type)
    db.commit()
    db.refresh(db_product_type)
    return db_product_type

def update_product_type(db: Session, product_type_id: int, product_type: ProductTypeUpdate):
    db_product_type = db.query(ProductType).filter(ProductType.id == product_type_id).first()
    if db_product_type:
        update_data = product_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product_type, key, value)
        db.commit()
        db.refresh(db_product_type)
    return db_product_type

def delete_product_type(db: Session, product_type_id: int):
    db_product_type = db.query(ProductType).filter(ProductType.id == product_type_id).first()
    if db_product_type:
        db.delete(db_product_type)
        db.commit()
    return db_product_type
