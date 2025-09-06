import uuid
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List, Any

from pydantic import BaseModel, Field


# --- Warehouse Schemas ---
class WarehouseBase(BaseModel):
    # public_id = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False, index=True)
    name: str
    code: str
    address: Optional[str] = None
    # status = Column(String(50), default='active')
    # temperature_type_id = Column(Integer, ForeignKey('temperature_types.id'), nullable=True)
    temperature_type_id: Optional[int] = None

class WarehouseCreate(WarehouseBase):
    # 'public_id' is server-generated.
    # 'status' has a server-side default.
    pass

class WarehouseUpdate(WarehouseBase):
    """
    Schema for updating an existing Warehouse record.
    All fields are optional, allowing for partial updates.
    Use model_dump(exclude_unset=True) when converting to dict for update.
    """
    name: Optional[str] = None
    code: Optional[str] = None
    address: Optional[str] = None
    temperature_type_id: Optional[int] = None

class WarehouseInDBBase(WarehouseBase):
    id: int
    public_id: uuid.UUID # Mapped from String(36) UUID
    status: str = Field(default='active') # Corresponds to SQLAlchemy default value

    # Relationships
    # temperature_type = relationship('TemperatureType', back_populates='warehouses')
    # Note: 'TemperatureType' model is not provided, so its Pydantic schema is undefined.
    # Using Any as a placeholder for the relationship object.
    temperature_type: Optional[Any] = None
    racks: List['Rack'] = [] # Relationship to Rack, using forward reference

    class Config:
        from_attributes = True

class Warehouse(WarehouseInDBBase):
    pass

# --- Rack Schemas ---
class RackBase(BaseModel):
    # public_id = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False, index=True)
    code: str
    # quantity = Column(Integer, default=0, nullable=False)
    # status = Column(String(50), default='active')
    
    # Location details
    zone: Optional[str] = None  # Zone A, B, C
    row: Optional[str] = None   # Row 1, 2, 3
    level: Optional[str] = None # Level 1, 2, 3
    
    warehouse_id: int
    # allocation_id = Column(Integer, ForeignKey('allocations.id'), nullable=True)
    allocation_id: Optional[int] = None
    
    # location_type_id = Column(Integer, ForeignKey('location_types.id'), nullable=True)
    location_type_id: Optional[int] = None

class RackCreate(RackBase):
    # 'public_id' is server-generated.
    # 'quantity' has a server-side default.
    # 'status' has a server-side default.
    pass

class RackUpdate(RackBase):
    """
    Schema for updating an existing Rack record.
    All fields are optional, allowing for partial updates.
    Use model_dump(exclude_unset=True) when converting to dict for update.
    """
    code: Optional[str] = None
    zone: Optional[str] = None
    row: Optional[str] = None
    level: Optional[str] = None
    warehouse_id: Optional[int] = None
    allocation_id: Optional[int] = None
    location_type_id: Optional[int] = None

class RackInDBBase(RackBase):
    id: int
    public_id: uuid.UUID # Mapped from String(36) UUID
    quantity: int = Field(default=0) # Corresponds to SQLAlchemy default value
    status: str = Field(default='active') # Corresponds to SQLAlchemy default value

    # Relationships
    warehouse: 'Warehouse' # Many-to-one relationship to Warehouse, using forward reference
    # allocation = relationship('Allocation', back_populates='racks')
    # Note: 'Allocation' model is not provided, so its Pydantic schema is undefined.
    # Using Any as a placeholder for the relationship object.
    allocation: Optional[Any] = None
    allocations: List['RackAllocation'] = [] # Relationship to RackAllocation, using forward reference

    # location_type = relationship('LocationType')
    # Note: 'LocationType' model is not provided, so its Pydantic schema is undefined.
    # Using Any as a placeholder for the relationship object.
    location_type: Optional[Any] = None

    class Config:
        from_attributes = True

class Rack(RackInDBBase):
    pass

# --- RackAllocation Schemas ---
class RackAllocationBase(BaseModel):
    # rack_id = Column(Integer, ForeignKey('racks.id'), nullable=False)
    rack_id: int
    # allocation_id = Column(Integer, ForeignKey('allocations.id'), nullable=False)
    allocation_id: int
    
    quantity: int
    
    # placement_date = Column(DateTime, default=func.current_timestamp())
    placed_by: Optional[str] = None
    position_details: Optional[str] = None

class RackAllocationCreate(RackAllocationBase):
    # 'placement_date' has a server-side default.
    pass

class RackAllocationUpdate(RackAllocationBase):
    """
    Schema for updating an existing RackAllocation record.
    All fields are optional, allowing for partial updates.
    Use model_dump(exclude_unset=True) when converting to dict for update.
    """
    rack_id: Optional[int] = None
    allocation_id: Optional[int] = None
    quantity: Optional[int] = None
    placed_by: Optional[str] = None
    position_details: Optional[str] = None

class RackAllocationInDBBase(RackAllocationBase):
    id: int
    placement_date: datetime # Corresponds to SQLAlchemy default func.current_timestamp()

    # Relationships
    rack: 'Rack' # Many-to-one relationship to Rack, using forward reference
    # allocation = relationship('Allocation', back_populates='rack_allocations')
    # Note: 'Allocation' model is not provided, so its Pydantic schema is undefined.
    # Using Any as a placeholder for the relationship object.
    allocation: Any

    class Config:
        from_attributes = True

class RackAllocation(RackAllocationInDBBase):
    pass


# Rebuild forward references for models to resolve circular dependencies
Warehouse.model_rebuild()
Rack.model_rebuild()
RackAllocation.model_rebuild()