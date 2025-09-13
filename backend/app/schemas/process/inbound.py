# file: app/schemas/process/inbound.py (FINAL & COMPLETE)

from typing import Optional, List , Annotated 
from pydantic import BaseModel, Field, model_validator, ConfigDict
from decimal import Decimal
from datetime import date, datetime
import uuid

# Impor skema lain yang dibutuhkan
from ..product.product import ProductCreate
from ..type.allocation_type import AllocationType
from ..type.product_type import ProductType
from ..type.package_type import PackageType
from ..type.temperature_type import TemperatureType
from ..warehouse.rack import Rack as RackSchema
from ..product.allocation import Allocation as AllocationSchema
from ..product.batch import Batch as BatchSchema

# --- Skema untuk Data Persiapan Form ---

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

class InboundPayload(BaseModel):
    """Payload tunggal dan lengkap untuk mengeksekusi proses inbound."""
    existing_product_id: Optional[int] = None
    new_product_data: Optional[ProductCreate] = None
    
    # ✅ SEKARANG MENGGUNAKAN SKEMA YANG LEBIH LENGKAP
    batch_data: InboundBatchData
    
    placement_data: InboundPlacementData
    allocation_type_id: int = Field(..., description="ID dari tipe alokasi tujuan, misal: REGULAR_STOCK.")

    @model_validator(mode='before')
    @classmethod
    def check_product_source(cls, data):
        # ... (validator tetap sama) ...
        if data.get('existing_product_id') and data.get('new_product_data'):
            raise ValueError("Hanya boleh menyediakan 'existing_product_id' atau 'new_product_data', tidak keduanya.")
        if not data.get('existing_product_id') and not data.get('new_product_data'):
            raise ValueError("Salah satu dari 'existing_product_id' atau 'new_product_data' wajib diisi.")
        return data
# --- Skema untuk Respons Proses ---

class InboundResponse(BaseModel):
    """
    Respons lengkap setelah proses inbound berhasil.
    Mewarisi dari StockPlacement dan menambahkan relasi yang dalam.
    """
    id: int
    public_id: uuid.UUID
    quantity: int
    placement_date: datetime
    
    # Relasi yang di-eager load dan diserialisasi
    rack: RackSchema
    allocation: AllocationSchema

    model_config = ConfigDict(from_attributes=True)