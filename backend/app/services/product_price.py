from sqlalchemy.orm import Session
from app.models.type import ProductPrice
from app.schemas.product_price import ProductPriceCreate, ProductPriceUpdate

def get_product_price(db: Session, product_price_id: int):
    return db.query(ProductPrice).filter(ProductPrice.id == product_price_id).first()

def get_product_prices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProductPrice).offset(skip).limit(limit).all()

def create_product_price(db: Session, product_price: ProductPriceCreate):
    db_product_price = ProductPrice(**product_price.dict())
    db.add(db_product_price)
    db.commit()
    db.refresh(db_product_price)
    return db_product_price

def update_product_price(db: Session, product_price_id: int, product_price: ProductPriceUpdate):
    db_product_price = db.query(ProductPrice).filter(ProductPrice.id == product_price_id).first()
    if db_product_price:
        update_data = product_price.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product_price, key, value)
        db.commit()
        db.refresh(db_product_price)
    return db_product_price

def delete_product_price(db: Session, product_price_id: int):
    db_product_price = db.query(ProductPrice).filter(ProductPrice.id == product_price_id).first()
    if db_product_price:
        db.delete(db_product_price)
        db.commit()
    return db_product_price
