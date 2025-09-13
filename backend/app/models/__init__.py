# file: app/models/__init__.py (REFACTORED & AUDITED)

# --- [BAGIAN 1: IMPOR MODEL] ---
# Mengimpor semua komponen yang dibutuhkan oleh Alembic dan aplikasi.

# Konfigurasi dasar, Enum, dan Tipe
from .configuration import (
    TimestampMixin, PublicIDMixin, BaseModel,
    AddressTypeEnum, WarehouseStatusEnum, RackStatusEnum, AllocationStatusEnum,
    SalesOrderStatusEnum, ShippingPlanStatusEnum, MovementDirectionEnum,
    ProductType, PackageType, TemperatureType, AllocationType, SectorType,
    CustomerType, DocumentType, StatusType, LocationType, PackagingMaterial,
    PackagingBoxType, PriorityLevel, NotificationType, DeliveryType,
    ProductPrice, MovementType,
    sales_order_item_sector_association,
    sales_order_item_allocation_association,
)

# Model Proses Pemesanan
from .order_process import (
    SalesOrder, SalesOrderItem,
    ShippingPlan, ShippingPlanItem
)

# Model Inti Produk & Stok
from .product import (
    Product,
    Batch,
    Allocation
)

# Model Pengguna & Pelanggan
from .users import (
    Customer,
    CustomerAddress
)

# Model Gudang
from .warehouse import (
    Warehouse,
    Rack,
    StockPlacement
)

# Model Proses Bisnis (Konsinyasi & Tender)
# PENTING: Pastikan file-file ini sudah direfaktor ke sintaks Mapped/mapped_column!
from .process import (
    Consignment, ConsignmentAgreement,
    ConsignmentItem, ConsignmentReturn,
    ConsignmentSale, ConsignmentStatement,
    TenderContract, ContractReservation
)


# --- [BAGIAN 2: API PUBLIK MODUL (`__all__`)] ---
# Daftar ini mengontrol apa yang diekspos dan dilihat oleh Alembic.
# Semua kesalahan sintaks dan typo telah diperbaiki.

__all__ = [
    # Mixins & Base
    "TimestampMixin", "PublicIDMixin", "BaseModel",

    # Enums
    "AddressTypeEnum", "WarehouseStatusEnum", "RackStatusEnum",
    "AllocationStatusEnum", "SalesOrderStatusEnum", "ShippingPlanStatusEnum",
    "MovementDirectionEnum",

    # Tipe (Lookup Tables)
    "ProductType", "PackageType", "TemperatureType", "AllocationType",
    "SectorType", "CustomerType", "DocumentType", "StatusType",
    "LocationType", "PackagingMaterial", "PackagingBoxType",
    "PriorityLevel", "NotificationType", "DeliveryType", "ProductPrice",
    "MovementType",

    # Tabel Asosiasi
    "sales_order_item_sector_association",
    "sales_order_item_allocation_association",

    # Warehouse
    "Warehouse", "Rack", "StockPlacement", # <-- FIXED: "Racks" -> "Rack"

    # Users
    "Customer", "CustomerAddress",

    # Product
    "Product", "Batch", "Allocation",

    # Order Process
    "SalesOrder", "SalesOrderItem", "ShippingPlan", "ShippingPlanItem",

    # Consignment Process
    "Consignment", "ConsignmentAgreement", "ConsignmentItem",
    "ConsignmentReturn", "ConsignmentSale", "ConsignmentStatement",

    # Tender Process
    "TenderContract", "ContractReservation",
]