from datetime import datetime
from sqlalchemy import (
    Integer, String, ForeignKey, Text, Enum as SQLAlchemyEnum, UniqueConstraint, DateTime, func
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from typing import List, Optional

from ..configuration import BaseModel, WarehouseStatusEnum, RackStatusEnum
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..configuration import TemperatureType, LocationType
    from ..product import Allocation
    from .warehouse import Warehouse
    from .rack import Rack

class StockPlacement(BaseModel):
    __tablename__ = 'stock_placements'
    rack_id: Mapped[int] = mapped_column(ForeignKey('racks.id'), nullable=False)
    allocation_id: Mapped[int] = mapped_column(ForeignKey('allocations.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    placed_by: Mapped[Optional[str]] = mapped_column(String(50))
    placement_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    rack: Mapped['Rack'] = relationship(back_populates='placement')
    allocation: Mapped['Allocation'] = relationship(back_populates='placements')
    __table_args__ = (UniqueConstraint('rack_id', name='uq_rack_id_placement'),)