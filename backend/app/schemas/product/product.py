# file: app/schemas/product/product.py

import uuid
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated

# Impor skema lain yang dibutuhkan untuk relasi
from ..type.product_type import ProductType
from ..type.package_type import PackageType
from ..type.temperature_type import TemperatureType
from ..type.product_price import ProductPrice

# ✅ FIXED: Use TYPE_CHECKING for potential circular references
if TYPE_CHECKING:
    from .batch import Batch
    from ..order_process.sales_order_item import SalesOrderItem

# --- Product Schemas ---

class ProductBase(BaseModel):
    """Skema dasar dengan field yang dapat diinput oleh pengguna."""
    product_code: Annotated[str, Field(..., max_length=25, description="Unique product code or SKU.")]
    name: Annotated[str, Field(..., max_length=100, description="Product name.")]
    manufacturer: Optional[str] = Field(None, max_length=100)
    product_type_id: int
    package_type_id: int
    temperature_type_id: int

class ProductCreate(ProductBase):
    """Skema untuk membuat produk baru. Saat ini sama dengan Base."""
    pass

class ProductUpdate(BaseModel):
    """Skema untuk memperbarui produk. Semua field opsional."""
    product_code: Optional[Annotated[str, Field(max_length=25)]] = None
    name: Optional[Annotated[str, Field(max_length=100)]] = None
    manufacturer: Optional[str] = None
    product_type_id: Optional[int] = None
    package_type_id: Optional[int] = None
    temperature_type_id: Optional[int] = None

class Product(ProductBase):
    """Skema read untuk Product, termasuk field dari server dan relasi."""
    id: int
    public_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    # Relasi yang di-load
    product_type: Optional[ProductType] = None
    package_type: Optional[PackageType] = None
    temperature_type: Optional[TemperatureType] = None
    prices: List[ProductPrice] = []
    batches: List['Batch'] = [] # Hindari relasi dua arah yang dalam jika tidak perlu
    sales_order_items: List['SalesOrderItem'] = []

    model_config = ConfigDict(from_attributes=True)

class ProductInBatch(ProductBase):
    """
    Skema read sederhana untuk Product saat ditampilkan SEBAGAI BAGIAN DARI Batch.
    Skema ini TIDAK menyertakan relasi `batches` untuk memutus lingkaran.
    """
    id: int
    public_id: uuid.UUID
    
    # Anda bisa menyertakan relasi tipe jika perlu
    product_type: Optional[ProductType] = None
    package_type: Optional[PackageType] = None
    temperature_type: Optional[TemperatureType] = None

    model_config = ConfigDict(from_attributes=True)    