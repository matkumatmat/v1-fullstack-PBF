# file: app/schemas/process/inbound.py (FINAL & COMPLETE)
from typing import Optional, List, Annotated
from pydantic import BaseModel, Field, model_validator, ConfigDict
from decimal import Decimal
from datetime import date, datetime
import uuid

# Impor skema-skema dasar yang kita butuhkan
from ..product.product import ProductCreate, ProductBase
from ..type.allocation_type import AllocationType
from ..type.product_type import ProductType
from ..type.package_type import PackageType
from ..type.temperature_type import TemperatureType
from ..warehouse.rack import RackBase
from ..product.allocation import AllocationBase
from ..product.batch import BatchBase
from ..warehouse.stock_placement import StockPlacementBase
from app.models.configuration import AllocationStatusEnum, RackStatusEnum

# --- Skema untuk Data Persiapan Form ---

class ProductTypeLookUp(BaseModel):
    public_id : uuid.UUID
    


class InboundFormData(BaseModel):
    """Data yang dibutuhkan frontend untuk membangun form inbound."""
    allocation_types: List[AllocationType]
    product_types: List[ProductType]
    package_types: List[PackageType]
    temperature_types: List[TemperatureType]

class InboundProductSearchSchema(BaseModel):
    """Respons sederhana untuk pencarian produk."""
    id: int
    product_code: str
    name: str
    model_config = {"from_attributes": True}

class InboundRackSearchSchema(BaseModel):
    """Respons sederhana untuk pencarian rak."""
    id: int
    code: str
    # Mengambil kode warehouse dari relasi
    warehouse_code: str = Field(..., alias="warehouse.code")
    current_quantity: int
    model_config = {"from_attributes": True}

class InboundBatchData(BaseModel):
    """
    Data spesifik untuk Batch yang diterima.
    ✅ DIPERBAIKI: Sekarang menyertakan field opsional untuk dimensi dan berat.
    """
    # Data Wajib
    lot_number: str = Field(..., max_length=50)
    expiry_date: date
    NIE: str = Field(..., max_length=50)
    received_quantity: Annotated[int, Field(gt=0)]
    receipt_document: str = Field(..., max_length=25)
    receipt_date: date
    
    # Data Opsional (diisi saat inbound jika tersedia)
    receipt_pic: Optional[str] = Field(None, max_length=25)
    receipt_doc_url: Optional[str] = Field(None, max_length=255)
    length: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    width: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    height: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    weight: Optional[Decimal] = Field(None, max_digits=10, decimal_places=3)

class InboundPlacementData(BaseModel):
    """Data spesifik untuk penempatan awal."""
    rack_id: int
    quantity: Annotated[int, Field(gt=0)]

# file: app/schemas/process/inbound.py (PAYLOAD YANG DISIMPLIFIKASI)

import uuid
from typing import Optional, List, Annotated
from pydantic import BaseModel, Field, model_validator
from datetime import date
from decimal import Decimal

from ..product.product import ProductCreate

class InboundPayload(BaseModel):
    """
    Payload yang ramping dan datar untuk proses inbound.
    """
    # --- Informasi Produk ---
    # Klien menyediakan salah satu dari dua ini.
    existing_product_public_id: Optional[uuid.UUID] = Field(None, description="Public ID dari produk yang sudah ada.")
    new_product_data: Optional[ProductCreate] = Field(None, description="Data untuk membuat produk baru jika belum ada.")

    # --- Informasi Batch ---
    # Semua data batch digabungkan langsung ke payload utama.
    lot_number: str = Field(..., max_length=50)
    expiry_date: date
    NIE: str = Field(..., max_length=50)
    received_quantity: Annotated[int, Field(gt=0)]
    receipt_document: str = Field(..., max_length=25)
    receipt_date: date
    
    # Data Batch Opsional
    length: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    width: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    height: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    weight: Optional[Decimal] = Field(None, max_digits=10, decimal_places=3)

    # --- Informasi Penempatan ---
    rack_public_id: uuid.UUID = Field(..., description="Public ID dari rak tujuan.")
    placement_quantity: Annotated[int, Field(gt=0)]

    # --- Informasi Tujuan Bisnis ---
    allocation_type_public_id: uuid.UUID = Field(..., description="Public ID dari tipe alokasi tujuan (misal: REGULAR_STOCK).")

    @model_validator(mode='before')
    @classmethod
    def check_product_source(cls, data):
        if data.get('existing_product_public_id') and data.get('new_product_data'):
            raise ValueError("Hanya boleh menyediakan 'existing_product_public_id' atau 'new_product_data', tidak keduanya.")
        if not data.get('existing_product_public_id') and not data.get('new_product_data'):
            raise ValueError("Salah satu dari 'existing_product_public_id' atau 'new_product_data' wajib diisi.")
        return data
    
class BatchInResponse(BatchBase):
    """Representasi Batch yang aman di dalam respons, tidak ada referensi balik."""
    id: int
    public_id: uuid.UUID
    # Tidak ada field 'product' atau 'allocations' yang dalam untuk mencegah rekursi

    model_config = ConfigDict(from_attributes=True)

class AllocationInResponse(AllocationBase):
    """Representasi Allocation yang aman di dalam respons."""
    id: int
    public_id: uuid.UUID
    status: AllocationStatusEnum
    
    batch: BatchInResponse # Menggunakan skema Batch yang aman
    allocation_type: AllocationType
    # Perhatikan: TIDAK ADA field 'placements' di sini. Ini memutus lingkaran.

    model_config = ConfigDict(from_attributes=True)

class RackInResponse(RackBase):
    """Representasi Rack yang aman di dalam respons."""
    id: int
    public_id: uuid.UUID
    status: RackStatusEnum
    # Perhatikan: TIDAK ADA field 'placement' di sini. Ini memutus lingkaran.

    model_config = ConfigDict(from_attributes=True)

# file: app/schemas/process/inbound.py (RESPONS YANG DISIMPLIFIKASI)

# ... (definisi payload di atas) ...
from pydantic import ConfigDict

class InboundResponse(BaseModel):
    """
    Respons yang ringkas dan informatif setelah proses inbound berhasil.
    Hanya berisi identifier publik dari entitas yang dibuat.
    """
    product_public_id: uuid.UUID
    batch_public_id: uuid.UUID
    allocation_public_id: uuid.UUID
    stock_placement_public_id: uuid.UUID
    
    message: str = "Proses inbound berhasil. Stok menunggu persetujuan QC."

    model_config = ConfigDict(from_attributes=False) # Tidak perlu from_attributes jika kita membangunnya secara manual