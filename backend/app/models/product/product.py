from datetime import date
from sqlalchemy import (
    String, ForeignKey,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from ..configuration import BaseModel

# Impor tipe relasi untuk type hinting
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..configuration import ProductType, PackageType, TemperatureType, ProductPrice
    from ..order_process import SalesOrderItem
    from .batch import Batch


class Product(BaseModel):
    __tablename__ = 'products'
    product_code: Mapped[str] = mapped_column(String(25), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    manufacturer: Mapped[Optional[str]] = mapped_column(String(100))
    product_type_id: Mapped[int] = mapped_column(ForeignKey('product_types.id'), nullable=False)
    package_type_id: Mapped[int] = mapped_column(ForeignKey('package_types.id'), nullable=False)
    temperature_type_id: Mapped[int] = mapped_column(ForeignKey('temperature_types.id'), nullable=False)

    batches: Mapped[List['Batch']] = relationship(back_populates='product')
    product_type: Mapped['ProductType'] = relationship(back_populates='products')
    package_type: Mapped['PackageType'] = relationship(back_populates='products')     
    temperature_type: Mapped['TemperatureType'] = relationship(back_populates='products')
    sales_order_items: Mapped[List['SalesOrderItem']] = relationship(back_populates='product')
    prices: Mapped[List['ProductPrice']] = relationship(back_populates='product', cascade='all, delete-orphan')
    def __repr__(self) -> str:
        return f"<Product(id={self.id})>"
