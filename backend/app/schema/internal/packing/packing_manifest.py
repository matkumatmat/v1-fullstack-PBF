# file: app/schemas/internal/packing/manifest_schemas.py

import uuid
from typing import List, Optional
from pydantic import BaseModel, Field

from app.schema.base import FePlBase, FeResBase

# --- SKEMA INPUT (PAYLOAD) ---

class PackedItemCreate(BaseModel):
    product: str
    batch: str
    expire_date: str
    quantity: str
    unit: str

class PackedBoxCreate(BaseModel):
    box_number: int = Field(..., alias='id') # Terima 'id' dari frontend, tapi pake 'box_number' di internal
    petugas: Optional[str] = None
    berat: Optional[str] = None
    items: List[PackedItemCreate]
    # sscc dan gtin dari frontend kita hiraukan, jadi nggak perlu ada di sini

class ContentCreate(BaseModel):
    total_box: int
    packing_slip: Optional[str] = None
    boxes: List[PackedBoxCreate] = Field(..., alias='box_number') # Terima 'box_number' sebagai list

class LocationInfoCreate(BaseModel):
    location_public_id: uuid.UUID = Field(..., alias='locations_id')
    tujuan_kirim: str
    # ... field lain dari "locations" kalo perlu ...

class PackingManifestCreate(FePlBase):
    locations: LocationInfoCreate
    content: ContentCreate

# --- SKEMA RESPONSE ---

class PackedItemResponse(BaseModel):
    product: str
    batch: str
    expire_date: str
    quantity: str
    unit: str
    class Config: from_attributes = True

class PackedBoxResponse(FeResBase):
    box_number: int
    sscc: str
    gtin: str
    petugas: Optional[str]
    berat: Optional[str]
    packed_items: List[PackedItemResponse]

class PackingManifestResponse(FeResBase):
    location_public_id: uuid.UUID
    tujuan_kirim: str
    packing_slip: Optional[str]
    total_boxes: int
    packed_boxes: List[PackedBoxResponse]

class LabelAddressData(BaseModel):
    """Struktur data alamat yang sudah diolah untuk label."""
    line_1: str
    line_2: Optional[str] = None
    line_3: Optional[str] = None
    province: str
    city: str
    pic_contact: str

class LabelDataResponse(FeResBase):
    """
    Response lengkap berisi semua data yang dibutuhkan untuk mencetak satu set label
    dari sebuah manifest.
    """
    manifest_public_id: uuid.UUID
    packing_slip: Optional[str]
    tujuan_kirim: str
    
    # Alamat pengirim yang sudah diolah
    shipping_address: LabelAddressData
    
    # Data kotak-kotak yang akan dicetak (kita bisa pake ulang skema yang ada)
    packed_boxes: List[PackedBoxResponse]    