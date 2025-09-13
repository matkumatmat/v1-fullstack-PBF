# file: app/schemas/__init__.py (FINAL SOLUTION)

# --- [BAGIAN 1: IMPOR EKSPLISIT SEMUA SKEMA] ---
# Langkah ini sangat penting. Kita membawa semua kelas skema ke dalam
# namespace (scope) dari file __init__.py ini.

# Customer
from .customer.customer import Customer, CustomerCreate, CustomerUpdate
from .customer.customer_address import CustomerAddress, CustomerAddressCreate, CustomerAddressUpdate

# Product
from .product.product import Product, ProductCreate, ProductUpdate, ProductInBatch
from .product.batch import Batch, BatchCreate, BatchUpdate
from .product.allocation import Allocation, AllocationCreate, AllocationUpdate

# Warehouse
from .warehouse.warehouse import Warehouse, WarehouseCreate, WarehouseUpdate
from .warehouse.rack import Rack, RackCreate, RackUpdate, RackInPlacement
from .warehouse.stock_placement import StockPlacement, StockPlacementCreate, StockPlacementUpdate, PlacementInRack

# Order Process
from .order_process.sales_order import SalesOrder, SalesOrderCreate, SalesOrderUpdate
from .order_process.sales_order_item import SalesOrderItem, SalesOrderItemCreate, SalesOrderItemUpdate
from .order_process.shipping_plan import ShippingPlan, ShippingPlanCreate, ShippingPlanUpdate
from .order_process.shipping_plan_item import ShippingPlanItem, ShippingPlanItemCreate, ShippingPlanItemUpdate

# Process-specific Schemas
from .process.inbound import InboundPayload, InboundResponse
from .process.consignment import Consignment, ConsignmentItem, ConsignmentReallocationPayload, ConsignmentItemPayload
from .process.tender import TenderReallocationPayload

# Types
from .type import (
    ProductType, ProductTypeCreate, ProductTypeUpdate,
    PackageType, PackageTypeCreate, PackageTypeUpdate,
    TemperatureType, TemperatureTypeCreate, TemperatureTypeUpdate,
    AllocationType, AllocationTypeCreate, AllocationTypeUpdate,
    SectorType, SectorTypeCreate, SectorTypeUpdate,
    CustomerType, CustomerTypeCreate, CustomerTypeUpdate,
    DocumentType, DocumentTypeCreate, DocumentTypeUpdate,
    StatusType, StatusTypeCreate, StatusTypeUpdate,
    LocationType, LocationTypeCreate, LocationTypeUpdate,
    PackagingMaterial, PackagingMaterialCreate, PackagingMaterialUpdate,
    PackagingBoxType, PackagingBoxTypeCreate, PackagingBoxTypeUpdate,
    PriorityLevel, PriorityLevelCreate, PriorityLevelUpdate,
    NotificationType, NotificationTypeCreate, NotificationTypeUpdate,
    DeliveryType, DeliveryTypeCreate, DeliveryTypeUpdate,
    ProductPrice, ProductPriceCreate, ProductPriceUpdate,
    MovementType, MovementTypeCreate, MovementTypeUpdate,
)


# --- [BAGIAN 2: DEFINISI API PUBLIK (`__all__`)] ---
# Daftar ini mengontrol apa yang diimpor saat seseorang melakukan `from app.schemas import *`
__all__ = [
    # Customer
    "Customer", "CustomerCreate", "CustomerUpdate", "CustomerAddress", "CustomerAddressCreate", "CustomerAddressUpdate",
    # Product
    "Product", "ProductCreate", "ProductUpdate", "ProductInBatch", "Batch", "BatchCreate", "BatchUpdate", "Allocation", "AllocationCreate", "AllocationUpdate",
    # Warehouse
    "Warehouse", "WarehouseCreate", "WarehouseUpdate", "Rack", "RackCreate", "RackUpdate", "StockPlacement", "StockPlacementCreate", "StockPlacementUpdate","PlacementInRack","RackInPlacement",
    # Order Process
    "SalesOrder", "SalesOrderCreate", "SalesOrderUpdate", "SalesOrderItem", "SalesOrderItemCreate", "SalesOrderItemUpdate", "ShippingPlan", "ShippingPlanCreate", "ShippingPlanUpdate", "ShippingPlanItem", "ShippingPlanItemCreate", "ShippingPlanItemUpdate",
    # Process
    "InboundPayload", "InboundResponse", "Consignment", "ConsignmentItem", "ConsignmentReallocationPayload", "ConsignmentItemPayload", "TenderReallocationPayload",
    # Types
    "ProductType", "ProductTypeCreate", "ProductTypeUpdate", "PackageType", "PackageTypeCreate", "PackageTypeUpdate", "TemperatureType", "TemperatureTypeCreate", "TemperatureTypeUpdate", "AllocationType", "AllocationTypeCreate", "AllocationTypeUpdate", "SectorType", "SectorTypeCreate", "SectorTypeUpdate", "CustomerType", "CustomerTypeCreate", "CustomerTypeUpdate", "DocumentType", "DocumentTypeCreate", "DocumentTypeUpdate", "StatusType", "StatusTypeCreate", "StatusTypeUpdate", "LocationType", "LocationTypeCreate", "LocationTypeUpdate", "PackagingMaterial", "PackagingMaterialCreate", "PackagingMaterialUpdate", "PackagingBoxType", "PackagingBoxTypeCreate", "PackagingBoxTypeUpdate", "PriorityLevel", "PriorityLevelCreate", "PriorityLevelUpdate", "NotificationType", "NotificationTypeCreate", "NotificationTypeUpdate", "DeliveryType", "DeliveryTypeCreate", "DeliveryTypeUpdate", "ProductPrice", "ProductPriceCreate", "ProductPriceUpdate", "MovementType", "MovementTypeCreate", "MovementTypeUpdate",
]


def _rebuild_models_with_namespace():
    """
    Membangun namespace global dari semua skema yang diimpor dan kemudian
    merebuild setiap model dengan menyediakan namespace tersebut secara eksplisit.
    Ini menyelesaikan semua forward references bahkan dalam kasus impor melingkar yang kompleks.
    """
    print("🔄 Rebuilding Pydantic models with a shared global namespace...")

    types_namespace = {name: obj for name, obj in globals().items() if name in __all__}
    print(f"  ├── Created namespace with {len(types_namespace)} schema types.")

    rebuilt_count = 0
    # ✅ TAMBAHAN: Loop untuk mencetak nama model yang direbuild
    for name in __all__:
        model = types_namespace.get(name)
        if model and hasattr(model, 'model_rebuild'):
            try:
                # Mencetak nama model SEBELUM mencoba merebuild
                print(f"  ├── 🏗️  Rebuilding: {name}")
                model.model_rebuild(_types_namespace=types_namespace)
                rebuilt_count += 1
            except Exception as e:
                print(f"  └── ❌ FATAL: Error rebuilding '{name}': {e}")
                raise
    
    print(f"  └── ✅ Rebuilt {rebuilt_count} models successfully.")
# Jalankan fungsi rebuild.
_rebuild_models_with_namespace()


# --- [BAGIAN 4: CLEANUP] ---
# Hapus fungsi helper dari namespace modul.
del _rebuild_models_with_namespace