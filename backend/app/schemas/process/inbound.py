# file: app/schemas/process/inbound.py (VERSI DIPERBAIKI)

from typing import Optional, List
from pydantic import BaseModel, Field, model_validator

# Impor skema-skema dasar
from app.schemas.product.product import ProductCreate
from app.schemas.product.batch import BatchBase  # <-- Gunakan Base, bukan Create
from app.schemas.product.allocation import AllocationBase # <-- Gunakan Base, bukan Create
from app.schemas.warehouse.stock_placement import StockPlacement
from app.schemas.type.allocation_type import AllocationType
from app.schemas.type.product_type import ProductType
from app.schemas.type.package_type import PackageType
from app.schemas.type.temperature_type import TemperatureType

# ... (Skema InboundFormData, InboundProductSearchSchema, InboundRackSearchSchema tidak berubah) ...
class InboundFormData(BaseModel):
    allocation_types: List[AllocationType]
    product_types: List[ProductType]
    package_types: List[PackageType]
    temperature_types: List[TemperatureType]

class InboundProductSearchSchema(BaseModel):
    id: int
    product_code: str
    name: str
    model_config = {"from_attributes": True}

class InboundRackSearchSchema(BaseModel):
    id: int
    code: str
    warehouse_code: str = Field(..., alias="warehouse.code")
    current_quantity: int
    model_config = {"from_attributes": True}

# --- SKEMA SPESIFIK UNTUK PAYLOAD INBOUND ---

class InboundBatchData(BatchBase):
    """Skema Batch khusus untuk payload inbound. Menghilangkan product_id."""
    model_config = {
        "exclude": {"product_id"}
    }

class InboundAllocationData(AllocationBase):
    """Skema Alokasi khusus untuk payload inbound. Menghilangkan batch_id."""
    model_config = {
        "exclude": {"batch_id"}
    }

class InboundPayload(BaseModel):
    """
    Skema payload tunggal dan lengkap untuk mengeksekusi proses inbound.
    Menggunakan skema turunan untuk kontrak API yang lebih bersih.
    """
    product_id: Optional[int] = Field(None, description="ID dari produk yang sudah ada.")
    new_product_data: Optional[ProductCreate] = Field(None, description="Data lengkap untuk membuat produk baru.")
    
    ### PERBAIKAN DI SINI ###
    batch_data: InboundBatchData = Field(..., description="Data untuk batch baru yang diterima.")
    allocation_data: InboundAllocationData = Field(..., description="Data untuk alokasi awal stok dari batch ini.")
    
    rack_id: int = Field(..., description="ID dari Rack tujuan untuk penempatan stok awal.")
    placement_quantity: int = Field(..., gt=0, description="Jumlah yang akan ditempatkan di rak.")

    @model_validator(mode='before')
    @classmethod
    def check_product_source(cls, data):
        # ... (validator ini tidak berubah) ...
        product_id_present = 'product_id' in data and data.get('product_id') is not None
        new_product_data_present = 'new_product_data' in data and data.get('new_product_data') is not None
        if product_id_present and new_product_data_present:
            raise ValueError("Hanya boleh menyediakan 'product_id' atau 'new_product_data', tidak keduanya.")
        if not product_id_present and not new_product_data_present:
            raise ValueError("Salah satu dari 'product_id' atau 'new_product_data' wajib diisi.")
        return data

class InboundResponse(StockPlacement):
    pass