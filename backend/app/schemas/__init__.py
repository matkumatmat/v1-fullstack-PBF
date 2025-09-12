# file: app/schemas/__init__.py (COMPLETELY FIXED)

# --- [BAGIAN 1: IMPOR MODUL] ---
# Impor semua sub-modul dalam urutan dependency yang benar
# Tidak ada circular dependency karena semua sudah menggunakan TYPE_CHECKING

from . import customer
from . import product
from . import warehouse
from . import order_process
from . import type as type_schemas
from . import process

# --- [BAGIAN 2: DEFINISI API PUBLIK (`__all__`)] ---
__all__ = [
    # Customer
    "Customer", "CustomerCreate", "CustomerUpdate",
    "CustomerAddress", "CustomerAddressCreate", "CustomerAddressUpdate",
    # Product
    "Product", "ProductCreate", "ProductUpdate","ProductInBatch",
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

    "consignment"
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
def _rebuild_all_models():
    """
    Rebuild semua model dengan secara eksplisit menyediakan namespace yang lengkap
    ke setiap panggilan model_rebuild(), yang merupakan cara yang benar dan kuat.
    """
    print("🔄 Rebuilding Pydantic models with a shared namespace...")

    # Step 1: Buat satu namespace kamus yang komprehensif.
    # Ini berisi semua kelas skema yang mungkin digunakan sebagai forward references.
    # Kita menggunakan globals() dari modul ini karena _populate_namespace sudah mengisinya.
    types_namespace = {name: globals()[name] for name in __all__ if name in globals()}
    print(f"  ├── Created namespace with {len(types_namespace)} types.")

    # Step 2: Tentukan urutan model yang akan direbuild.
    # Urutannya sekarang jauh lebih tidak kritis, tetapi urutan logis tetap baik.
    all_models = [
        product.ProductInBatch,
        # Core
        product.Product, customer.Customer, warehouse.Warehouse,
        # Details
        product.Batch, customer.CustomerAddress, warehouse.Rack,
        # Linking
        product.Allocation, warehouse.StockPlacement,
        # Order Process
        order_process.SalesOrder, order_process.SalesOrderItem,
        order_process.ShippingPlan, order_process.ShippingPlanItem,
    ]

    # Step 3: Rebuild setiap model, dengan memberikan namespace yang lengkap.
    try:
        for model in all_models:
            # Pastikan model ada sebelum mencoba merebuild
            if model:
                print(f"  ├── Rebuilding {model.__name__}...")
                # ✅ INI ADALAH KUNCINYA: Berikan namespace secara langsung.
                model.model_rebuild(_types_namespace=types_namespace)

        print("  └── ✅ All models rebuilt successfully!")

    except Exception as e:
        print(f"  └── ❌ Error during model rebuild: {e}")
        import traceback
        traceback.print_exc()
        raise

_rebuild_all_models()


# --- [BAGIAN 5: CLEANUP] ---
del _populate_namespace, _rebuild_all_models