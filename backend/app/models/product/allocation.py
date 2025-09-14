from datetime import date
from sqlalchemy import (
    Integer, String, ForeignKey, Date, Numeric, Text,
    Enum as SQLAlchemyEnum
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

from ..configuration import BaseModel,AllocationStatusEnum
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..configuration import AllocationType
    from ..order_process import SalesOrderItem
    from ..users import Customer
    from ..warehouse import RackItem
    from .batch import Batch
    from ..process import Consignment
    from ..process import TenderContract

class Allocation(BaseModel):
    __tablename__ = 'allocations'
    allocated_quantity: Mapped[int] = mapped_column(Integer, default=0, server_default=0, active_history=True, info={'check': 'allocated_quantity >= 0'}) 
    shipped_quantity: Mapped[int] = mapped_column(Integer, default=0, server_default=0, active_history=True, info={'check': 'shipped_quantity >= 0'})   
    reserved_quantity: Mapped[int] = mapped_column(Integer, default=0, server_default=0, active_history=True, info={'check': 'reserved_quantity >= 0'})
    status: Mapped[AllocationStatusEnum] = mapped_column(SQLAlchemyEnum(AllocationStatusEnum, name="allocation_status_enum", create_type=False), default=AllocationStatusEnum.ACTIVE)
    allocation_number: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True, index=True)
    batch_id: Mapped[int] = mapped_column(ForeignKey('batches.id'), nullable=False)
    allocation_type_id: Mapped[int] = mapped_column(ForeignKey('allocation_types.id'), nullable=False)
    customer_id: Mapped[Optional[int]] = mapped_column(ForeignKey('customers.id'))
    original_reserved_quantity: Mapped[int] = mapped_column(Integer, default=0)
    customer_allocated_quantity: Mapped[int] = mapped_column(Integer, default=0)
    batch: Mapped['Batch'] = relationship(back_populates='allocations')
    allocation_type: Mapped['AllocationType'] = relationship(back_populates='allocations')
    customer: Mapped[Optional['Customer']] = relationship(back_populates='allocations')  
    placements: Mapped[List['RackItem']] = relationship(back_populates='racks_allocations')
    # picking_order_items: Mapped[List['PickingOrderItem']] = relationship(back_populates='allocation')
    # picking_list_items: Mapped[List['PickingListItem']] = relationship(back_populates='allocation')
    consignments: Mapped[List['Consignment']] = relationship(back_populates='allocation')
    # stock_movements: Mapped[List['StockMovement']] = relationship(back_populates='allocation')
    #tender_contract_id: Mapped[Optional[int]] = mapped_column(ForeignKey('tender_contracts.id'))
    #tender_contract: Mapped[Optional['TenderContract']] = relationship(back_populates='allocations')
    def __repr__(self) -> str:
        return f"<Allocation(id={self.id})>"
