from .type import (
    SectorType, AllocationType,
    sales_order_item_sector_association,
    sales_order_item_allocation_association
)
# file: app/models/order_process.py

from datetime import date, datetime
from sqlalchemy import (
    Integer, String, ForeignKey, Text, Date, Numeric, Boolean,
    Enum as SQLAlchemyEnum, Table, DateTime
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

# Impor komponen dasar dan Enum yang relevan
from .base import BaseModel
from .enums import SalesOrderStatusEnum, ShippingPlanStatusEnum

# Impor tipe relasi untuk type hinting yang lebih baik.
# Menggunakan `__future__` import style untuk menghindari circular import issues jika diperlukan.
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .customer import Customer
    from .product import Product
    from .type import (
        SectorType, AllocationType, ProductPrice
    )
    # Placeholder untuk model yang belum ada
    # class TenderContract: pass
    # class PackingOrder: pass
    # class PickingList: pass
    # class Shipment: pass
    # class PickingListItem: pass


class SalesOrder(BaseModel):
    __tablename__ = 'sales_order'
    
    # public_id, id, created_at, updated_at diwarisi dari BaseModel.
    # public_id = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False, index=True) # <-- DIGANTIKAN OLEH MIXIN

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