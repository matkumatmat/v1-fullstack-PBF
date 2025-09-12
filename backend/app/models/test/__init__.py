# file: app/models/__init__.py

# --- Fondasi dan Enum ---
from .base import BaseModel
from .enums import (
    AddressTypeEnum,
    WarehouseStatusEnum,
    RackStatusEnum,
    AllocationStatusEnum,
    SalesOrderStatusEnum,
    ShippingPlanStatusEnum,
    MovementDirectionEnum,
)

# --- Entitas Utama ---
from .customer import Customer, CustomerAddress
from .product import Product, Batch, Allocation
from .warehouse import Warehouse, Rack, StockPlacement # <-- DIUBAH: RackAllocation -> StockPlacement

# --- Proses Bisnis ---
from .order_process import SalesOrder, SalesOrderItem, ShippingPlan, ShippingPlanItem

# --- Tipe dan Data Master (Lookup Tables) ---
from .type import (
    ProductType,
    PackageType,
    TemperatureType,
    AllocationType,
    SectorType,
    CustomerType,
    DocumentType,
    StatusType,
    LocationType,
    PackagingMaterial,
    PackagingBoxType,
    PriorityLevel,
    NotificationType,
    DeliveryType,
    ProductPrice,
    MovementType,
    sales_order_item_sector_association,      # <-- DITAMBAHKAN: Ekspor tabel asosiasi
    sales_order_item_allocation_association,  # <-- DITAMBAHKAN: Ekspor tabel asosiasi
)

# `__all__` mendefinisikan API publik dari modul ini.
# Ini adalah daftar string nama yang akan diimpor ketika
# seseorang melakukan `from app.models import *`.
__all__ = [
    # Fondasi
    "BaseModel",
    
    # Entitas Utama
    "Customer",
    "CustomerAddress",
    "Product",
    "Batch",
    "Allocation",
    "Warehouse",
    "Rack",
    "StockPlacement",  # <-- DIUBAH: RackAllocation -> StockPlacement
    
    # Proses Bisnis
    "SalesOrder",
    "SalesOrderItem",
    "ShippingPlan",
    "ShippingPlanItem",
    
    # Tipe dan Data Master
    "ProductType",
    "PackageType",
    "TemperatureType",
    "AllocationType",
    "SectorType",
    "CustomerType",
    "DocumentType",
    "StatusType",
    "LocationType",
    "PackagingMaterial",
    "PackagingBoxType",
    "PriorityLevel",
    "NotificationType",
    "DeliveryType",
    "ProductPrice",
    "MovementType",
    
    # Tabel Asosiasi
    "sales_order_item_sector_association",
    "sales_order_item_allocation_association",

    # Enum (Sangat berguna untuk diakses dari seluruh aplikasi)
    "AddressTypeEnum",
    "WarehouseStatusEnum",
    "RackStatusEnum",
    "AllocationStatusEnum",
    "SalesOrderStatusEnum",
    "ShippingPlanStatusEnum",
    "MovementDirectionEnum",

    ### DEVIL'S ADVOCATE NOTE ###
    # Model `User` tidak didefinisikan atau diimpor di mana pun dalam file yang diberikan.
    # Saya menghapusnya dari `__all__` untuk mencegah ImportError.
    # Jika Anda memiliki file `user.py`, Anda harus mengimpornya di atas.
    # Contoh: from .user import User
    # "User", 
]