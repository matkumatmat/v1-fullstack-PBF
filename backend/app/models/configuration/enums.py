import enum

class AddressTypeEnum(str, enum.Enum):
    DISTRIBUTOR = "DISTRIBUTOR"
    CUSTOMER = "CUSTOMER"
    OFFICE = "OFFICE"
    WAREHOUSE = "WAREHOUSE"
    MANUFACTURER = "MANUFACTURER"

class WarehouseStatusEnum(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    MAINTENANCE = "MAINTENANCE"

class RackStatusEnum(str, enum.Enum):
    ACTIVE = "ACTIVE"
    MAINTENANCE = "MAINTENANCE"
    FULL = "FULL"

class AllocationStatusEnum(str, enum.Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"

class BatchStatusEnum(str, enum.enum):
    QUARANTINE ="QUARANTINE"
    ACTIVE ="ACTIVE"
    ALLOCATED ="ALLOCATED"
    EXPIRED ="EXPIRED"
    ON_HOLD ="ON_HOLD"

class SalesOrderStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    PARTIALLY_SHIPPED = "PARTIALLY_SHIPPED"
    CANCELLED = "CANCELLED"
    
class ShippingPlanStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class MovementDirectionEnum(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"
    TRANSFER = "TRANSFER"

class PackagingEnum(str, enum.enum):
    PACKAGING_MATERIAL="PACKAGING_MATERIAL"
    PACKAGING_BOX="PACKAGING_BOX"



    