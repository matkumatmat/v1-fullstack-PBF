from ..configuration import (
    SectorType, AllocationType,
    sales_order_item_sector_association,
    sales_order_item_allocation_association,
    BaseModel,SalesOrderStatusEnum,ShippingPlanStatusEnum
)
from datetime import date, datetime
from sqlalchemy import (
    Integer, String, ForeignKey, Text, Date, Numeric, Boolean,
    Enum as SQLAlchemyEnum, Table, DateTime
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..users import Customer
    from ..product import Product
    from ..configuration import (
        SectorType, AllocationType, ProductPrice
    )
    from .sales_order import SalesOrder, SalesOrderItem

class ShippingPlan(BaseModel):
    __tablename__ = 'shipping_plan'
    
    # public_id = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False, index=True) # <-- DIGANTIKAN OLEH MIXIN
    
    plan_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    planned_delivery_date: Mapped[date] = mapped_column(Date, nullable=False)
    actual_delivery_date: Mapped[Optional[date]] = mapped_column(Date)
    sales_order_id: Mapped[int] = mapped_column(ForeignKey('sales_order.id'), nullable=False)
    shipping_method: Mapped[Optional[str]] = mapped_column(String(50))
    status: Mapped[ShippingPlanStatusEnum] = mapped_column(SQLAlchemyEnum(ShippingPlanStatusEnum, name="shipping_plan_status_enum", create_type=False), default=ShippingPlanStatusEnum.PENDING, nullable=False)
    created_by: Mapped[Optional[str]] = mapped_column(String(50))
    
    # created_date = Column(DateTime, default=func.current_timestamp()) # <-- DIKOMENTARI: Redundan dengan `created_at` dari BaseModel. Sebaiknya dihapus.
    
    confirmed_by: Mapped[Optional[str]] = mapped_column(String(50))
    confirmed_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    delivery_address: Mapped[Optional[str]] = mapped_column(Text)
    contact_person: Mapped[Optional[str]] = mapped_column(String(100))
    contact_phone: Mapped[Optional[str]] = mapped_column(String(20))

    # --- Relationships ---
    sales_order: Mapped['SalesOrder'] = relationship(back_populates='shipping_plans')
    items: Mapped[List['ShippingPlanItem']] = relationship(back_populates='shipping_plan', cascade='all, delete-orphan')
    
    # Merefaktor relasi yang dikomentari ke sintaks modern.
    # picking_lists: Mapped[List['PickingList']] = relationship(back_populates='shipping_plan')
    # shipment: Mapped[Optional['Shipment']] = relationship(back_populates='shipping_plan', uselist=False)

    @property
    def total_quantity(self) -> int:
        """Total quantity dalam shipping plan"""
        return sum(item.quantity_to_fulfill for item in self.items)
    
    @property
    def total_products(self) -> int:
        """Total jenis produk dalam shipping plan"""
        return len(self.items)
    
    @property
    def has_picking_list(self) -> bool:
        """Apakah sudah ada picking list"""
        # `picking_lists` tidak didefinisikan, properti ini akan error.
        # Saya asumsikan ini akan diaktifkan saat relasi `picking_lists` diaktifkan.
        # return len(self.picking_lists) > 0
        return False # Placeholder aman untuk saat ini
    
    def __repr__(self) -> str:
        return f'<ShippingPlan id={self.id} plan_number="{self.plan_number}">'

class ShippingPlanItem(BaseModel):
    __tablename__ = 'shipping_plan_items'
    
    quantity_to_fulfill: Mapped[int] = mapped_column(Integer, nullable=False)
    shipping_plan_id: Mapped[int] = mapped_column(ForeignKey('shipping_plan.id'), nullable=False)
    sales_order_item_id: Mapped[int] = mapped_column(ForeignKey('sales_order_items.id'), nullable=False)
    line_number: Mapped[Optional[int]] = mapped_column(Integer)
    planned_date: Mapped[Optional[date]] = mapped_column(Date)
    status: Mapped[ShippingPlanStatusEnum] = mapped_column(SQLAlchemyEnum(ShippingPlanStatusEnum, name="shipping_plan_status_enum", create_type=False), default=ShippingPlanStatusEnum.PENDING)
    
    # --- Relationships ---
    shipping_plan: Mapped['ShippingPlan'] = relationship(back_populates='items')
    sales_order_item: Mapped['SalesOrderItem'] = relationship(back_populates='shipping_plan_items')
    
    # Merefaktor relasi yang dikomentari ke sintaks modern.
    # picking_list_items: Mapped[List['PickingListItem']] = relationship(back_populates='shipping_plan_item')
    
    ### DEVIL'S ADVOCATE NOTE ###
    # Properti yang melintasi beberapa relasi (`self.sales_order_item.product`) sangat berbahaya
    # karena dapat memicu beberapa lazy load (JOIN) secara berurutan.
    # Ini adalah kandidat utama untuk dioptimalkan dengan `selectinload` di query Anda.
    @property
    def product(self) -> Optional['Product']:
        """Get product dari SO item"""
        return self.sales_order_item.product if self.sales_order_item else None
    
    @property
    def sales_order(self) -> Optional['SalesOrder']:
        """Get sales order dari SO item"""
        return self.sales_order_item.sales_order if self.sales_order_item else None
    
    @property
    def customer(self) -> Optional['Customer']:
        """Get customer dari shipping plan"""
        return self.shipping_plan.sales_order.customer if self.shipping_plan and self.shipping_plan.sales_order else None
    
    @property
    def is_picking_list_created(self) -> bool:
        """Apakah sudah ada picking list untuk item ini"""
        # `picking_list_items` tidak didefinisikan, properti ini akan error.
        # Saya asumsikan ini akan diaktifkan saat relasi `picking_list_items` diaktifkan.
        # return len(self.picking_list_items) > 0
        return False # Placeholder aman untuk saat ini
    
    def __repr__(self) -> str:
        return f'<ShippingPlanItem id={self.id} plan_id={self.shipping_plan_id} so_item_id={self.sales_order_item_id}>'   