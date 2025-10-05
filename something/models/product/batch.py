from datetime import date
from sqlalchemy import (
    Integer, String, ForeignKey, Date, Numeric, text,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from ..configuration import BaseModel

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .product import Product
    from .allocation import Allocation

class Batch(BaseModel):
    __tablename__ = 'batches'
    lot_number: Mapped[str] = mapped_column(String(50), nullable=False)
    expiry_date: Mapped[date] = mapped_column(Date, nullable=False)
    NIE: Mapped[str] = mapped_column(String(50), nullable=False)
    received_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    receipt_document: Mapped[str] = mapped_column(String(25), nullable=False)
    receipt_date: Mapped[date] = mapped_column(Date, nullable=False)
    receipt_pic: Mapped[Optional[str]] = mapped_column(String(25))
    receipt_doc_url: Mapped[Optional[str]] = mapped_column(String(255))
    length: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    width: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    height: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    weight: Mapped[Optional[float]] = mapped_column(Numeric(10, 3))
    
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    product: Mapped['Product'] = relationship(back_populates='batches') 
    def __repr__(self) -> str:
        return f"<Batch(id={self.id})>"
