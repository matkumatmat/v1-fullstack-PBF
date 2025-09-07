# file: app/schemas/__init__.py (COMPLETELY FIXED)

# --- [BAGIAN 1: IMPOR MODUL] ---
# Impor semua sub-modul dalam urutan dependency yang benar
# Tidak ada circular dependency karena semua sudah menggunakan TYPE_CHECKING

from . import customer
from . import product
from . import warehouse
from . import order_process
from . import type as type_schemas

# --- [BAGIAN 2: DEFINISI API PUBLIK (`__all__`)] ---
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

# --- [BAGIAN 3: POPULATE NAMESPACE] ---
# ✅ FIXED: Lebih robust dan aman
def _populate_namespace():
    """
    Populate namespace dengan semua kelas dari modul-modul yang diimpor.
    Menggunakan pendekatan yang lebih robust daripada versi sebelumnya.
    """
    modules = {
        'customer': customer,
        'product': product, 
        'warehouse': warehouse,
        'order_process': order_process,
        'type_schemas': type_schemas
    }
    
    current_globals = globals()
    
    for name in __all__:
        found = False
        for module_name, module in modules.items():
            if hasattr(module, name):
                current_globals[name] = getattr(module, name)
                found = True
                break
        
        if not found:
            print(f"Warning: {name} not found in any module")

# Populate namespace
_populate_namespace()

# --- [BAGIAN 4: CENTRALIZED MODEL REBUILDING] ---
# ✅ FIXED: Satu tempat untuk semua model_rebuild(), dengan urutan yang benar

def _rebuild_all_models():
    """
    Rebuild semua model dengan forward references dalam urutan dependency yang benar.
    
    URUTAN PENTING:
    1. Base models dulu (tidak ada/sedikit dependencies)
    2. Models dengan relationships sedang
    3. Models dengan complex relationships terakhir
    """
    
    print("🔄 Rebuilding Pydantic models...")
    
    try:
        # Step 1: Base models dan Type models (tidak ada circular refs)
        print("  ├── Rebuilding base and type models...")
        # Type models sudah aman, tidak perlu rebuild khusus
        
        # Step 2: Core business models
        print("  ├── Rebuilding core models...")
        customer.Customer.model_rebuild()
        product.Product.model_rebuild()
        product.Batch.model_rebuild()
        warehouse.Warehouse.model_rebuild()
        warehouse.Rack.model_rebuild()
        
        # Step 3: Models dengan relationships ke core models
        print("  ├── Rebuilding relationship models...")
        customer.CustomerAddress.model_rebuild()
        product.Allocation.model_rebuild()
        warehouse.StockPlacement.model_rebuild()
        
        # Step 4: Order process models (paling kompleks)
        print("  ├── Rebuilding order process models...")
        order_process.SalesOrder.model_rebuild()
        order_process.SalesOrderItem.model_rebuild()
        order_process.ShippingPlan.model_rebuild()
        order_process.ShippingPlanItem.model_rebuild()
        
        print("  └── ✅ All models rebuilt successfully!")
        
    except Exception as e:
        print(f"  └── ❌ Error during model rebuild: {e}")
        raise

# ✅ CRITICAL: Jalankan rebuild setelah semua impor selesai
_rebuild_all_models()

# --- [BAGIAN 5: CLEANUP] ---
# Hapus fungsi helper dari namespace publik
del _populate_namespace, _rebuild_all_models