from sqlalchemy import (
    Integer, String, ForeignKey, Enum as SQLAlchemyEnum,
    func, select, UniqueConstraint, DateTime
)
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from typing import Optional
from ..configuration import BaseModel,RackStatusEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .warehouse import Warehouse
    from ..product import Allocation

class Rack(BaseModel):
    __tablename__ = 'racks'
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    status: Mapped[RackStatusEnum] = mapped_column(SQLAlchemyEnum(RackStatusEnum, name="rack_status_enum", create_type=False), default=RackStatusEnum.ACTIVE)
    column: Mapped[Optional[str]] = mapped_column(String(10))
    row: Mapped[Optional[str]] = mapped_column(String(10))
    level: Mapped[Optional[str]] = mapped_column(String(10))
    warehouse_id: Mapped[int] = mapped_column(ForeignKey('warehouses.id'), nullable=False)
    warehouse: Mapped['Warehouse'] = relationship(back_populates='racks')
    item: Mapped[Optional['RackItem']] = relationship(back_populates='rack', cascade="all, delete-orphan", uselist=False)
    def __repr__(self) -> str:
        return f"<Rack id={self.id} rack code={self.code}'>"
    
class RackItem(BaseModel):
    __tablename__ = 'rack_items'
    rack_id: Mapped[int] = mapped_column(ForeignKey('racks.id'), nullable=False)
    allocation_id: Mapped[int] = mapped_column(ForeignKey('allocations.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, active_history=True, server_default= 0, info={'check':'quantitiy >=0 '})
    placed_by: Mapped[Optional[str]] = mapped_column(String(50),active_history=True)
    placement_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    rack: Mapped['Rack'] = relationship(back_populates='item')
    allocation: Mapped['Allocation'] = relationship(back_populates='racks_allocations')
    __table_args__ = (UniqueConstraint('rack_id', 'allocation_id', name='uq_rack_allocation'),
                    #Index('idx_rack_item_quantity', 'quantity'),  # Untuk reporting
                    #Index('idx_placement_date', 'placement_date') # Untuk audit queries
    )  
    def __repr__(self) -> str:
        return f"<Rack id={self.id} produk={self.allocation.batch} quantity={self.quantity}'>"
