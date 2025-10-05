import enum
from datetime import date
from sqlalchemy import (
    String,
    ForeignKey,
    Enum as SQLAlchemyEnum,
    Integer, String, ForeignKey, Text, Date, Numeric, Boolean,
    UniqueConstraint   
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from ..configuration import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .batch import Batch

class ProductUnitEnum(str, enum.Enum):
    VIAL = "VIAL"
    AMPUL = "AMPUL"
    PFS = "PFS" 
    BOX= "BOX"
    PACK = "PACK"
    BOTTLE = "BOTOL"
    PCS = "PCS"
    DOSE = "DOSE"

class ProductTypeEnum(str, enum.Enum):
    VAKSIN = "VAKSIN"
    SERUM = "SERUM"
    KIT = "KIT DIAGNOSTIK"
    ALKES = "ALKES"
    COMPLEMENTARY = "PENUNJANG"  

class TemperatureTypeEnum(str, enum.Enum):
    ROOM = "ROOM TEMPERATURE"
    COLD = "COLD TEMPERATURE"
    MINUS = "MINUS TEMPERATURE"
    EXTREME = "EXTREME TEMPERATURE"    

class ProductPrice(BaseModel):
    __tablename__ = 'product_prices'
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)
    HNA: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    HJP: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    HET: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    product: Mapped['Product'] = relationship(back_populates='prices')
    def __repr__(self) -> str:
        return f'<ProductPrice code="{self.id}" product_id={self.product_id}>'        

class Product(BaseModel):
    __tablename__ = 'products'
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    manufacturer: Mapped[Optional[str]] = mapped_column(String(100))

    type: Mapped[ProductTypeEnum] = mapped_column(
        SQLAlchemyEnum(ProductTypeEnum, name="product_type_enum", create_type=False), 
        nullable=False
    )
    unit: Mapped[ProductUnitEnum] = mapped_column(
        SQLAlchemyEnum(ProductUnitEnum, name="product_unit_enum", create_type=False), 
        nullable=False
    )
    temperature: Mapped[ProductTypeEnum] = mapped_column(
        SQLAlchemyEnum(ProductTypeEnum, name="product_temperature_enum", create_type=False), 
        nullable=False
    )

    batches: Mapped[List['Batch']] = relationship(back_populates='product')
    prices: Mapped[List['ProductPrice']] = relationship(back_populates='product', cascade='all, delete-orphan')
    def __repr__(self) -> str:
        return f"<Product(id={self.id})>"
