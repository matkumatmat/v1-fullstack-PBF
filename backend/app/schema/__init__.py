from .base import *
from .type import (
    allocation_type, customer_type, delivery_type, document_type,
    movement_type, notification_type, package_type, packaging_material,
    product_price, product_type, sector_type, status_type, temperature_type
)

from .internal.product.product import (
    _ProductCore, ProductFePl, ProductFePlUpdate,
    ProductFeRes, ProductFeResLookup, ProductDb
)
from .internal.product.batch import (
    _BatchCore, BatchFePl, BatchFePlUpdate,
    BatchFeRes, BatchDb, BatchSummary,
)
from .internal.product.allocation import (
    _AllocationCore, AllocationFePl, AllocationFePlUpdate,
    AllocationFeRes, AllocationDb
)



__all__=[
    "_Base", "_WithDbMixin","_PublicIdentifierMixin",
    "_InternalIdentifierMixin","_TimestampMixin"
    "FeResBase","FeResLookup","FePlBase","FePlUpdate","DbBase"

    "allocation_type", "customer_type", "delivery_type", "document_type",
    "movement_type", "notification_type", "package_type", "packaging_material",
    "product_price", "product_type", "sector_type", "status_type", "temperature_type"

    "_ProductCore","ProductFePl","ProductFePlUpdate","ProductFeRes","ProductFeResLookup","ProductDb",    

    "_BatchCore","BatchFePl","BatchFePlUpdate","BatchFeRes","BatchDb","BatchSummary",

    "_AllocationCore","AllocationFePl","AllocationFePlUpdate","AllocationFeRes","AllocationDb",        
]


def _rebuild_models_with_namespace():
    """
    Membangun namespace global dari semua skema yang diimpor dan kemudian
    merebuild setiap model dengan menyediakan namespace tersebut secara eksplisit.
    """
    print("Rebuilding Pydantic models with a shared global namespace...")

    types_namespace = {name: obj for name, obj in globals().items() if name in __all__}
    print(f"  ├── Created namespace with {len(types_namespace)} schema types.")

    # Hanya daftarkan skema yang menggunakan Forward References (string literals).
    # Biasanya ini adalah skema Read (...FeRes) dan skema Internal (...Db).
    models_to_rebuild = [
        ProductFeRes,
        ProductDb,
        BatchFeRes,
        BatchDb,
        AllocationFeRes,
        AllocationDb,
        
        # yang memiliki relasi bersarang dengan forward reference.
        # Contoh:
        # CustomerFeRes,
        # WarehouseFeRes,
        # RackFeRes,
    ]

    rebuilt_count = 0
    for model in models_to_rebuild:
        if model and hasattr(model, 'model_rebuild'):
            try:
                print(f"  ├── >>>> Rebuilding: {model.__name__}")
                model.model_rebuild(_types_namespace=types_namespace)
                rebuilt_count += 1
            except Exception as e:
                print(f"  └── xxxx FATAL: Error rebuilding '{model.__name__}': {e}")
                raise
    
    print(f"  └── Rebuilt {rebuilt_count} models successfully.")

_rebuild_models_with_namespace()
del _rebuild_models_with_namespace