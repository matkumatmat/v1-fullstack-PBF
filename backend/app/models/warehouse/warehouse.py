from sqlalchemy import (String, ForeignKey, Text, Enum as SQLAlchemyEnum)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from ..configuration import BaseModel, WarehouseStatusEnum
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..configuration import TemperatureType
    from .rack import Rack
    
class Warehouse(BaseModel):
    __tablename__ = 'warehouses'
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    address: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[WarehouseStatusEnum] = mapped_column(SQLAlchemyEnum(WarehouseStatusEnum, name="warehouse_status_enum", create_type=False), default=WarehouseStatusEnum.ACTIVE)
    temperature_type_id: Mapped[Optional[int]] = mapped_column(ForeignKey('temperature_types.id'))
    temperature_type: Mapped[Optional['TemperatureType']] = relationship(back_populates='warehouses')
    racks: Mapped[List['Rack']] = relationship(back_populates='warehouse')
