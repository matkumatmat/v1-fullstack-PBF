# file: app/models/packing/manifest.py

from __future__ import annotations
from sqlalchemy import (
    String, ForeignKey, Integer, Text
)
import uuid
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from typing import List, Optional, Dict, Any, TYPE_CHECKING

from ..configuration import BaseModel
if TYPE_CHECKING:
    from ..users.customer import Location

class PackingManifest(BaseModel):
    __tablename__ = 'packing_manifests'
    
    location_id: Mapped[int] = mapped_column(ForeignKey('locations.id'), nullable=False)
    shipping_to_location_public_id: uuid.UUID # Lokasi TUJUAN
    packing_slip: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    total_boxes: Mapped[int] = mapped_column(Integer)
    shipping_address_details: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    shipping_to_location_id: Mapped[int] = mapped_column(ForeignKey('locations.id'), nullable=False)
    
    
    location: Mapped[Location] = relationship(foreign_keys=[location_id])
    shipping_to_location: Mapped[Location] = relationship(foreign_keys=[shipping_to_location_id])
    packed_boxes: Mapped[List[PackedBox]] = relationship(
        back_populates='manifest', cascade='all, delete-orphan'
    )

class PackedBox(BaseModel):
    __tablename__ = 'packed_boxes'
    
    manifest_id: Mapped[int] = mapped_column(ForeignKey('packing_manifests.id'), nullable=False)
    box_number: Mapped[int] = mapped_column(Integer)
    sscc: Mapped[str] = mapped_column(String(18), unique=True, index=True)
    gtin: Mapped[str] = mapped_column(String(8))
    petugas: Mapped[Optional[str]] = mapped_column(String(50))
    berat: Mapped[Optional[str]] = mapped_column(String(20))
    
    manifest: Mapped[PackingManifest] = relationship(back_populates='packed_boxes')
    packed_items: Mapped[List[PackedItem]] = relationship(
        back_populates='box', cascade='all, delete-orphan'
    )

class PackedItem(BaseModel):
    __tablename__ = 'packed_items'
    
    box_id: Mapped[int] = mapped_column(ForeignKey('packed_boxes.id'), nullable=False)
    product: Mapped[str] = mapped_column(String(100))
    batch: Mapped[str] = mapped_column(String(50))
    expire_date: Mapped[str] = mapped_column(String(20))
    quantity: Mapped[str] = mapped_column(String(20))
    unit: Mapped[str] = mapped_column(String(20))
    
    box: Mapped[PackedBox] = relationship(back_populates='packed_items')