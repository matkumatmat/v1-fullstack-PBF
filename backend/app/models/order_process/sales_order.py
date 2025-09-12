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
        SectorType, AllocationType, ProductPrice)
    from .shipping_plan import ShippingPlan, ShippingPlanItem
    

class SalesOrder(BaseModel):
    __tablename__ = 'sales_order'
    
    so_number: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=False)
    so_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_amount: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    
    status: Mapped[SalesOrderStatusEnum] = mapped_column(SQLAlchemyEnum(SalesOrderStatusEnum, name="sales_order_status_enum", create_type=False), default=SalesOrderStatusEnum.PENDING, nullable=False)
    
    input_by: Mapped[Optional[str]] = mapped_column(String(50))
    notes: Mapped[Optional[str]] = mapped_column(Text)
    special_instructions: Mapped[Optional[str]] = mapped_column(Text)
    is_tender_so: Mapped[bool] = mapped_column(Boolean, default=False)

    # --- Relationships ---
    customer: Mapped['Customer'] = relationship(back_populates='sales_orders')
    items: Mapped[List['SalesOrderItem']] = relationship(back_populates='sales_order', cascade='all, delete-orphan')
    
    ### DEVIL'S ADVOCATE NOTE ###
    # Mengubah nama relasi dari `shipping_plan` menjadi `shipping_plans` dan tipe menjadi `List[]`
    # untuk secara akurat merepresentasikan hubungan One-to-Many (satu SO bisa punya banyak rencana pengiriman).
    shipping_plans: Mapped[List['ShippingPlan']] = relationship(back_populates='sales_order')
    
    ### DEVIL'S ADVOCATE NOTE ###
    # Merefaktor field yang dikomentari ke sintaks modern.
    # Saat Anda siap menggunakannya, Anda hanya perlu menghapus komentar.
    # tender_contract_id: Mapped[Optional[int]] = mapped_column(ForeignKey('tender_contracts.id'))
    # tender_contract: Mapped[Optional['TenderContract']] = relationship(back_populates='sales_order')
    # packing_orders: Mapped[List['PackingOrder']] = relationship(back_populates='sales_order')
    
    ### DEVIL'S ADVOCATE NOTE ###
    # Properti ini nyaman tetapi memiliki risiko performa N+1 yang signifikan.
    # Gunakan dengan hati-hati dan pertimbangkan untuk menghitung nilai-nilai ini
    # dalam query SQL untuk performa yang lebih baik pada dataset besar.
    @property
    def so_type(self) -> str:
        return 'TENDER' if self.is_tender_so else 'REGULAR'    
    
    @property
    def total_quantity_requested(self) -> int:
        """Total quantity dari semua items dalam SO"""
        return sum(item.quantity_requested for item in self.items)
    
    @property
    def total_quantity_planned(self) -> int:
        """Total quantity yang sudah masuk shipping plan"""
        total = 0
        for item in self.items:
            total += sum(spi.quantity_to_fulfill for spi in item.shipping_plan_items)
        return total
    
    @property
    def is_fully_planned(self) -> bool:
        """Apakah SO sudah fully planned"""
        return self.total_quantity_planned >= self.total_quantity_requested
    
    def __repr__(self) -> str:
        return f'<SalesOrder id={self.id} so_number="{self.so_number}">'

class SalesOrderItem(BaseModel):
    __tablename__ = 'sales_order_items'
    
    line_number: Mapped[Optional[int]] = mapped_column(Integer)
    quantity_requested: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    total_price: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    sales_order_id: Mapped[int] = mapped_column(ForeignKey('sales_order.id'), nullable=False)
    required_delivery_date: Mapped[Optional[date]] = mapped_column(Date)
    status: Mapped[SalesOrderStatusEnum] = mapped_column(SQLAlchemyEnum(SalesOrderStatusEnum, name="sales_order_status_enum", create_type=False), default=SalesOrderStatusEnum.PENDING)
    price_type_code_used: Mapped[str] = mapped_column(String(20), nullable=False)
    product_price_id: Mapped[Optional[int]] = mapped_column(ForeignKey('product_prices.id'))

    # --- Relationships ---
    product: Mapped['Product'] = relationship(back_populates='sales_order_items')
    sales_order: Mapped['SalesOrder'] = relationship(back_populates='items')
    product_price_entry: Mapped[Optional['ProductPrice']] = relationship(back_populates='sales_order_items')
    shipping_plan_items: Mapped[List['ShippingPlanItem']] = relationship(back_populates='sales_order_item', cascade='all, delete-orphan')
    
    sectors: Mapped[List['SectorType']] = relationship(secondary=sales_order_item_sector_association, back_populates='sales_order_items')
    allocations: Mapped[List['AllocationType']] = relationship(secondary=sales_order_item_allocation_association, back_populates='sales_order_items')
    
    @property
    def quantity_planned(self) -> int:
        return sum(spi.quantity_to_fulfill for spi in self.shipping_plan_items)
    
    @property
    def quantity_remaining(self) -> int:
        return self.quantity_requested - self.quantity_planned
    
    @property
    def is_fully_planned(self) -> bool:
        return self.quantity_planned >= self.quantity_requested
    
    def __repr__(self) -> str:
        return f'<SalesOrderItem id={self.id} so_id={self.sales_order_id} product_id={self.product_id}>'
