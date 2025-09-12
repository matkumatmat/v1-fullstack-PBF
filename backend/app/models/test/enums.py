# app/models/enums.py  <-- BUAT FILE BARU INI

import enum

class AddressTypeEnum(str, enum.Enum):
    DELIVERY = "DELIVERY"
    BILLING = "BILLING"
    WAREHOUSE = "WAREHOUSE"

class WarehouseStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"

class RackStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    MAINTENANCE = "maintenance"
    DAMAGED = "damaged"
    FULL = "full"

class AllocationStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    CANCELLED = "cancelled"

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