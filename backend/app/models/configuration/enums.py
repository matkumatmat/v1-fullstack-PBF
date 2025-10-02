import enum

class AddressTypeEnum(str, enum.Enum):
    DISTRIBUTOR = "DISTRIBUTOR"
    CUSTOMER = "CUSTOMER"
    MANUFACTURER = "MANUFACTURER"

class RackStatusEnum(str, enum.Enum):
    ACTIVE = "ACTIVE"
    FULL = "FULL"
    RESERVED = "RESERVED"

class AllocationTypeEnum(str, enum.Enum):
    SWASTA = "SWASTA"
    TENDER = "TENDER"
    PEMERINTAH = "PEMERINTAH"
    BUFFER = "BUFFER"
    HIBAH = "HIBAH"

class BatchItemStatusEnum(str, enum.Enum):
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
    COMPLETE = "COMPLETE"
    
class ShippingStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    ON_PACKING = "ON_PACKING"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class MovementEnum(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"
    TRANSFER = "TRANSFER"

class PackagingEnum(str, enum.Enum):
    PACKAGING_MATERIAL="PACKAGING_MATERIAL"
    PACKAGING_BOX="PACKAGING_BOX"

class PackagetypeEnum(str, enum.Enum):
    CKS = "CKS"
    CKS2 = "CKS2"
    PU1 = "PU1"
    PU2 = "PU2"
    CK = "CK"

class SectorTypeEnum(str, enum.Enum):
    SWASTA = "SWASTA"    
    PEMERINTAH = "P2M"

class CustomerTypeEnum(str, enum.Enum)    :
    PEMERINTAH ="PEMERINTAH"
    DISTRIBUTOR = "DISTRIBUTOR"
    RETAIL = "RETAIL"

class ProductPriceEnum(str, enum.Enum)    :
    HJP = "HJP"
    HNA = "HNA"
    HET = "HET"

class TemperatureTypeEnum(str, enum.Enum):
    ROOM = "ROOM TEMPERATURE"
    COLD = "COLD TEMPERATURE"
    MINUS = "MINUS TEMPERATURE"
    EXTREME = "EXTREME TEMPERATURE"     




    