from sqlalchemy import (String, ForeignKey, Text, Enum as SQLAlchemyEnum)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from ..configuration import BaseModel, WarehouseStatusEnum, TemperatureTypeEnum
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..configuration import TemperatureTypeEnum
    from .rack import Rack
    
class Warehouse(BaseModel):
    __tablename__ = 'warehouses'
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(Text)
    temperature: Mapped[TemperatureTypeEnum] = mapped_column(SQLAlchemyEnum(TemperatureTypeEnum, name="temperature_type_enum", create_type=False), nullable=False)

    racks: Mapped[List['Rack']] = relationship(back_populates='warehouse')
