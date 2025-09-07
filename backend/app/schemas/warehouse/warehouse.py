# file: app/schemas/warehouse/warehouse.py

import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated

from app.models.enums import WarehouseStatusEnum
from ..type.temperature_type import TemperatureType
from .rack import Rack
from typing import TYPE_CHECKING


# --- Warehouse Schemas ---

class WarehouseBase(BaseModel):
    """Skema dasar dengan field yang dapat diinput oleh pengguna untuk Warehouse."""
    name: Annotated[str, Field(..., max_length=100)]
    code: Annotated[str, Field(..., max_length=10)]
    address: Optional[str] = None
    temperature_type_id: Optional[int] = None

class WarehouseCreate(WarehouseBase):
    """Skema untuk membuat Warehouse baru."""
    pass

class WarehouseUpdate(BaseModel):
    """Skema untuk memperbarui Warehouse. Semua field opsional."""
    name: Optional[Annotated[str, Field(max_length=100)]] = None
    code: Optional[Annotated[str, Field(max_length=10)]] = None
    address: Optional[str] = None
    temperature_type_id: Optional[int] = None
    status: Optional[WarehouseStatusEnum] = None

class Warehouse(WarehouseBase):
    """Skema read untuk Warehouse, termasuk field dari server dan relasi."""
    id: int
    public_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    status: WarehouseStatusEnum

    # Relasi yang di-load
    temperature_type: Optional[TemperatureType] = None
    racks: List['Rack'] = []

    model_config = ConfigDict(from_attributes=True)