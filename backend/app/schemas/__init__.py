# file: app/schemas/__init__.py (REFAKTORED)

# --- [BAGIAN 1: IMPOR MODUL] ---
# DEVIL'S ADVOCATE NOTE:
# Alih-alih mengimpor setiap kelas satu per satu, kita impor modulnya.
# Ini lebih bersih dan lebih mudah dikelola. Kita akan menggunakan `__all__`
# di bawah untuk mengontrol apa yang diekspos secara publik.
# Pastikan setiap sub-direktori (customer, product, dll.) memiliki `__init__.py`-nya sendiri.
from . import customer
from . import product
from . import warehouse
from . import order_process
from . import type as type_schemas

# --- [BAGIAN 2: REBUILDING FORWARD REFERENCES] ---
# DEVIL'S ADVOCATE NOTE:
# Ini adalah bagian paling KRITIS yang akan menyelesaikan error `PydanticUndefinedAnnotation`.
# Setelah semua modul di atas diimpor, semua kelas skema (Customer, Rack, Allocation, dll.)
# sudah ada di dalam memori. Sekarang adalah waktu yang aman untuk memberitahu Pydantic
# untuk menyelesaikan semua referensi string (misalnya, 'Allocation', 'Rack').

warehouse.Warehouse.model_rebuild()
warehouse.Rack.model_rebuild()
warehouse.StockPlacement.model_rebuild()
customer.Customer.model_rebuild()
product.Allocation.model_rebuild()
order_process.SalesOrder.model_rebuild()
order_process.SalesOrderItem.model_rebuild()
order_process.ShippingPlan.model_rebuild()
order_process.ShippingPlanItem.model_rebuild()


# --- [BAGIAN 3: DEFINISI API PUBLIK (`__all__`)] ---
# `__all__` mendefinisikan apa yang akan diimpor saat seseorang melakukan `from app.schemas import *`.
# Ini adalah cara yang baik untuk menjaga namespace tetap bersih.
__all__ = [
    # Customer
    "Customer", "CustomerCreate", "CustomerUpdate",
    "CustomerAddress", "CustomerAddressCreate", "CustomerAddressUpdate",
    # Product
    "Product", "ProductCreate", "ProductUpdate",
    "Batch", "BatchCreate", "BatchUpdate",
    "Allocation", "AllocationCreate", "AllocationUpdate",
    # Warehouse
    "Warehouse", "WarehouseCreate", "WarehouseUpdate",
    "Rack", "RackCreate", "RackUpdate",
    "StockPlacement", "StockPlacementCreate", "StockPlacementUpdate",
    # Order Process
    "SalesOrder", "SalesOrderCreate", "SalesOrderUpdate",
    "SalesOrderItem", "SalesOrderItemCreate", "SalesOrderItemUpdate",
    "ShippingPlan", "ShippingPlanCreate", "ShippingPlanUpdate",
    "ShippingPlanItem", "ShippingPlanItemCreate", "ShippingPlanItemUpdate",
    # Types
    "ProductType", "ProductTypeCreate", "ProductTypeUpdate",
    "PackageType", "PackageTypeCreate", "PackageTypeUpdate",
    "TemperatureType", "TemperatureTypeCreate", "TemperatureTypeUpdate",
    "AllocationType", "AllocationTypeCreate", "AllocationTypeUpdate",
    "SectorType", "SectorTypeCreate", "SectorTypeUpdate",
    "CustomerType", "CustomerTypeCreate", "CustomerTypeUpdate",
    "DocumentType", "DocumentTypeCreate", "DocumentTypeUpdate",
    "StatusType", "StatusTypeCreate", "StatusTypeUpdate",
    "LocationType", "LocationTypeCreate", "LocationTypeUpdate",
    "PackagingMaterial", "PackagingMaterialCreate", "PackagingMaterialUpdate",
    "PackagingBoxType", "PackagingBoxTypeCreate", "PackagingBoxTypeUpdate",
    "PriorityLevel", "PriorityLevelCreate", "PriorityLevelUpdate",
    "NotificationType", "NotificationTypeCreate", "NotificationTypeUpdate",
    "DeliveryType", "DeliveryTypeCreate", "DeliveryTypeUpdate",
    "ProductPrice", "ProductPriceCreate", "ProductPriceUpdate",
    "MovementType", "MovementTypeCreate", "MovementTypeUpdate",
]

# --- [BAGIAN 4: MEMBUAT `__all__` BEKERJA] ---
# DEVIL'S ADVOCATE NOTE:
# Agar `__all__` berfungsi dengan impor modular kita, kita perlu secara dinamis
# mengisi namespace `__init__.py` ini. Loop ini akan mengambil setiap kelas
# dari modul yang diimpor dan membuatnya tersedia secara langsung.
_module_names = ["customer", "product", "warehouse", "order_process", "type_schemas"]
for _name in __all__:
    for _mod_name in _module_names:
        _mod = locals()[_mod_name]
        if hasattr(_mod, _name):
            globals()[_name] = getattr(_mod, _name)
            break