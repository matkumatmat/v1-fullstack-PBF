from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.product_price import ProductPrice, ProductPriceCreate, ProductPriceUpdate
from app.services.product_price import (
    create_product_price,
    delete_product_price,
    get_product_price,
    get_product_prices,
    update_product_price,
)

router = APIRouter()

@router.post("/", response_model=ProductPrice)
def create_new_product_price(
    product_price: ProductPriceCreate, db: Session = Depends(get_db)
):
    return create_product_price(db=db, product_price=product_price)

@router.get("/{product_price_id}", response_model=ProductPrice)
def read_product_price(product_price_id: int, db: Session = Depends(get_db)):
    db_product_price = get_product_price(db, product_price_id=product_price_id)
    if db_product_price is None:
        raise HTTPException(status_code=404, detail="ProductPrice not found")
    return db_product_price

@router.get("/", response_model=List[ProductPrice])
def read_product_prices(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    product_prices = get_product_prices(db, skip=skip, limit=limit)
    return product_prices

@router.put("/{product_price_id}", response_model=ProductPrice)
def update_existing_product_price(
    product_price_id: int,
    product_price: ProductPriceUpdate,
    db: Session = Depends(get_db),
):
    db_product_price = update_product_price(
        db, product_price_id=product_price_id, product_price=product_price
    )
    if db_product_price is None:
        raise HTTPException(status_code=404, detail="ProductPrice not found")
    return db_product_price

@router.delete("/{product_price_id}", response_model=ProductPrice)
def delete_existing_product_price(
    product_price_id: int, db: Session = Depends(get_db)
):
    db_product_price = delete_product_price(db, product_price_id=product_price_id)
    if db_product_price is None:
        raise HTTPException(status_code=404, detail="ProductPrice not found")
    return db_product_price
