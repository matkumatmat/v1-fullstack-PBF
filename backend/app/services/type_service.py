# file: app/services/type_service.py

from app.models.configuration import (
    AllocationType,
    CustomerType,
    DeliveryType,
    DocumentType,
    LocationType,
    MovementType,
    NotificationType,
    PackageType,
    PackagingBoxType,
    PackagingMaterial,
    PriorityLevel,
    ProductPrice,
    ProductType,
    SectorType,
    StatusType,
    TemperatureType,
)
from app.schemas import (
    AllocationTypeCreate, AllocationTypeUpdate,
    CustomerTypeCreate, CustomerTypeUpdate,
    DeliveryTypeCreate, DeliveryTypeUpdate,
    DocumentTypeCreate, DocumentTypeUpdate,
    LocationTypeCreate, LocationTypeUpdate,
    MovementTypeCreate, MovementTypeUpdate,
    NotificationTypeCreate, NotificationTypeUpdate,
    PackageTypeCreate, PackageTypeUpdate,
    PackagingBoxTypeCreate, PackagingBoxTypeUpdate,
    PackagingMaterialCreate, PackagingMaterialUpdate,
    PriorityLevelCreate, PriorityLevelUpdate,
    ProductPriceCreate, ProductPriceUpdate,
    ProductTypeCreate, ProductTypeUpdate,
    SectorTypeCreate, SectorTypeUpdate,
    StatusTypeCreate, StatusTypeUpdate,
    TemperatureTypeCreate, TemperatureTypeUpdate,
)

from .base import CRUDBase

# --- Instance CRUD untuk setiap Tipe ---

allocation_type = CRUDBase[AllocationType, AllocationTypeCreate, AllocationTypeUpdate](AllocationType)
customer_type = CRUDBase[CustomerType, CustomerTypeCreate, CustomerTypeUpdate](CustomerType)
delivery_type = CRUDBase[DeliveryType, DeliveryTypeCreate, DeliveryTypeUpdate](DeliveryType)
document_type = CRUDBase[DocumentType, DocumentTypeCreate, DocumentTypeUpdate](DocumentType)
location_type = CRUDBase[LocationType, LocationTypeCreate, LocationTypeUpdate](LocationType)
movement_type = CRUDBase[MovementType, MovementTypeCreate, MovementTypeUpdate](MovementType)
notification_type = CRUDBase[NotificationType, NotificationTypeCreate, NotificationTypeUpdate](NotificationType)
package_type = CRUDBase[PackageType, PackageTypeCreate, PackageTypeUpdate](PackageType)
packaging_box_type = CRUDBase[PackagingBoxType, PackagingBoxTypeCreate, PackagingBoxTypeUpdate](PackagingBoxType)
packaging_material = CRUDBase[PackagingMaterial, PackagingMaterialCreate, PackagingMaterialUpdate](PackagingMaterial)
priority_level = CRUDBase[PriorityLevel, PriorityLevelCreate, PriorityLevelUpdate](PriorityLevel)
product_price = CRUDBase[ProductPrice, ProductPriceCreate, ProductPriceUpdate](ProductPrice)
product_type = CRUDBase[ProductType, ProductTypeCreate, ProductTypeUpdate](ProductType)
sector_type = CRUDBase[SectorType, SectorTypeCreate, SectorTypeUpdate](SectorType)
status_type = CRUDBase[StatusType, StatusTypeCreate, StatusTypeUpdate](StatusType)
temperature_type = CRUDBase[TemperatureType, TemperatureTypeCreate, TemperatureTypeUpdate](TemperatureType)