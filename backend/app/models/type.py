# file: app/models/type.py
from datetime import date
from sqlalchemy import (
    Integer, String, ForeignKey, Text, Date, Numeric, Boolean,
    UniqueConstraint, Table, Column, Enum as SQLAlchemyEnum 
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

# Impor komponen dasar dan Enum yang relevan
from .base import BaseModel
from .enums import MovementDirectionEnum

# Impor tipe relasi untuk type hinting
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .product import Product, Allocation
    from .warehouse import Warehouse
    from .customer import Customer
    from .order_process import SalesOrderItem
    # Placeholder untuk model yang belum ada
    # class ShipmentDocument: pass
    # class StockMovement: pass


# --- Tabel Asosiasi (Association Tables) ---
# Tidak ada perubahan besar di sini, hanya memastikan konsistensi.
sales_order_item_sector_association = Table(
    'so_item_sector_association',
    BaseModel.metadata,
    Column('sales_order_item_id', Integer, ForeignKey('sales_order_items.id'), primary_key=True),
    Column('sector_type_id', Integer, ForeignKey('sector_types.id'), primary_key=True)
)

sales_order_item_allocation_association = Table(
    'so_item_allocation_association',
    BaseModel.metadata,
    Column('sales_order_item_id', Integer, ForeignKey('sales_order_items.id'), primary_key=True),
    Column('allocation_type_id', Integer, ForeignKey('allocation_types.id'), primary_key=True)
)

# --- Model Tipe (Lookup Tables) ---

class ProductType(BaseModel):
    """Master data untuk jenis produk"""
    __tablename__ = 'product_types'
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    products: Mapped[List['Product']] = relationship(back_populates='product_type')
    
    def __repr__(self) -> str:
        return f'<ProductType code="{self.code}" name="{self.name}">'
    
class PackageType(BaseModel):
    __tablename__ = 'package_types'
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_fragile: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_stackable: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    max_stack_height: Mapped[Optional[int]] = mapped_column(Integer)
    special_handling_required: Mapped[bool] = mapped_column(Boolean, default=False)
    handling_instructions: Mapped[Optional[str]] = mapped_column(Text)

    products: Mapped[List['Product']] = relationship(back_populates='package_type')
    
    def __repr__(self) -> str:
        return f'<PackageType code="{self.code}" name="{self.name}">'    

class TemperatureType(BaseModel):
    __tablename__ = 'temperature_types'
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    ### DEVIL'S ADVOCATE NOTE ###
    # Mengganti `Float` dengan `Numeric` untuk data suhu. Ini memastikan presisi
    # dan menghindari kesalahan pembulatan yang bisa berakibat fatal dalam konteks farmasi/logistik.
    min_celsius: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))
    max_celsius: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))
    optimal_celsius: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))
    
    celsius_display: Mapped[Optional[str]] = mapped_column(String(20))
    humidity_range: Mapped[Optional[str]] = mapped_column(String(20))
    special_storage_requirements: Mapped[Optional[str]] = mapped_column(Text)
    color_code: Mapped[Optional[str]] = mapped_column(String(7))
    icon: Mapped[Optional[str]] = mapped_column(String(50))
    
    products: Mapped[List['Product']] = relationship(back_populates='temperature_type')
    warehouses: Mapped[List['Warehouse']] = relationship(back_populates='temperature_type')
    
    def __repr__(self) -> str:
        return f'<TemperatureType code="{self.code}" name="{self.name}">'

class AllocationType(BaseModel):
    __tablename__ = 'allocation_types'
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    color_code: Mapped[Optional[str]] = mapped_column(String(7))
    icon: Mapped[Optional[str]] = mapped_column(String(50))

    allocations: Mapped[List['Allocation']] = relationship(back_populates='allocation_type')
    sales_order_items: Mapped[List['SalesOrderItem']] = relationship(secondary=sales_order_item_allocation_association, back_populates='allocations')    
    
    def __repr__(self) -> str:
        return f'<AllocationType code="{self.code}" name="{self.name}">'
    
class SectorType(BaseModel):
    __tablename__ = 'sector_types'
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    requires_special_handling: Mapped[bool] = mapped_column(Boolean, default=False)
    default_payment_terms: Mapped[Optional[int]] = mapped_column(Integer)
    default_delivery_terms: Mapped[Optional[str]] = mapped_column(String(50))
    requires_temperature_monitoring: Mapped[bool] = mapped_column(Boolean, default=False)
    requires_chain_of_custody: Mapped[bool] = mapped_column(Boolean, default=False)
    special_documentation: Mapped[Optional[str]] = mapped_column(Text)
    
    customers: Mapped[List['Customer']] = relationship(back_populates='sector_type')
    sales_order_items: Mapped[List['SalesOrderItem']] = relationship(secondary=sales_order_item_sector_association, back_populates='sectors')    
    
    def __repr__(self) -> str:
        return f'<SectorType code="{self.code}" name="{self.name}">'
        
class CustomerType(BaseModel):
    __tablename__ = 'customer_types'
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    allows_tender_allocation: Mapped[bool] = mapped_column(Boolean, default=False)
    requires_pre_approval: Mapped[bool] = mapped_column(Boolean, default=False)
    default_credit_limit: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    default_discount_percent: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))
    default_payment_terms_days: Mapped[Optional[int]] = mapped_column(Integer, default=30)
    
    customers: Mapped[List['Customer']] = relationship(back_populates='customer_type')
    
    def __repr__(self) -> str:
        return f'<CustomerType code="{self.code}" name="{self.name}">'

class DocumentType(BaseModel):
    __tablename__ = 'document_types'
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=False)
    is_customer_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    max_file_size_mb: Mapped[int] = mapped_column(Integer, default=10)
    allowed_extensions: Mapped[Optional[str]] = mapped_column(String(100))
    auto_generate: Mapped[bool] = mapped_column(Boolean, default=False)
    template_path: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Merefaktor relasi yang dikomentari ke sintaks modern.
    # shipment_documents: Mapped[List['ShipmentDocument']] = relationship(back_populates='document_type')
    
    def __repr__(self) -> str:
        return f'<DocumentType code="{self.code}" name="{self.name}">'

class StatusType(BaseModel):
    __tablename__ = 'status_types'
    
    ### DEVIL'S ADVOCATE NOTE ###
    # Anda memilih pola Lookup Table untuk status. Ini memberikan fleksibilitas UI
    # dengan mengorbankan keamanan tipe statis (type-safety) yang diberikan oleh Enum Python.
    # Pastikan logika bisnis Anda selalu melakukan validasi terhadap `entity_type` dan `code`
    # untuk mencegah status yang tidak valid diterapkan ke entitas yang salah.
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_initial_status: Mapped[bool] = mapped_column(Boolean, default=False)
    is_final_status: Mapped[bool] = mapped_column(Boolean, default=False)
    is_error_status: Mapped[bool] = mapped_column(Boolean, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    color_code: Mapped[Optional[str]] = mapped_column(String(7))
    icon: Mapped[Optional[str]] = mapped_column(String(50))
    css_class: Mapped[Optional[str]] = mapped_column(String(50))
    auto_transition_after_hours: Mapped[Optional[int]] = mapped_column(Integer)
    requires_approval: Mapped[bool] = mapped_column(Boolean, default=False)
    sends_notification: Mapped[bool] = mapped_column(Boolean, default=False)
    
    __table_args__ = (UniqueConstraint('entity_type', 'code', name='uq_status_entity_code'),)
    
    def __repr__(self) -> str:
        return f'<StatusType {self.entity_type}.{self.code}: {self.name}>'

class LocationType(BaseModel):
    __tablename__ = 'location_types'
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_storage_location: Mapped[bool] = mapped_column(Boolean, default=True)
    is_picking_location: Mapped[bool] = mapped_column(Boolean, default=True)
    is_staging_location: Mapped[bool] = mapped_column(Boolean, default=False)
    
    max_weight_capacity_kg: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    supports_temperature_control: Mapped[bool] = mapped_column(Boolean, default=False)
    requires_special_access: Mapped[bool] = mapped_column(Boolean, default=False)
    
    def __repr__(self) -> str:
        return f'<LocationType code="{self.code}" name="{self.name}">'

class PackagingMaterial(BaseModel):
    __tablename__ = 'packaging_materials'
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    material_type: Mapped[Optional[str]] = mapped_column(String(20))
    is_reusable: Mapped[bool] = mapped_column(Boolean, default=False)
    is_fragile_protection: Mapped[bool] = mapped_column(Boolean, default=False)
    is_temperature_protection: Mapped[bool] = mapped_column(Boolean, default=False)

    length_cm: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    width_cm: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    height_cm: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    weight_g: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))

    cost_per_unit: Mapped[Optional[float]] = mapped_column(Numeric(8, 2))
    
    def __repr__(self) -> str:
        return f'<PackagingMaterial code="{self.code}" name="{self.name}">'
    
class PackagingBoxType(BaseModel):
    __tablename__ = 'packaging_box_types'
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    material_type: Mapped[Optional[str]] = mapped_column(String(20))
    is_reusable: Mapped[bool] = mapped_column(Boolean, default=False)
    is_fragile_protection: Mapped[bool] = mapped_column(Boolean, default=False)
    is_temperature_protection: Mapped[bool] = mapped_column(Boolean, default=False)

    length_cm: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    width_cm: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    height_cm: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    weight_g: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))

    cost_per_unit: Mapped[Optional[float]] = mapped_column(Numeric(8, 2))
    
    def __repr__(self) -> str:
        return f'<PackagingBoxType code="{self.code}" name="{self.name}">'    

class PriorityLevel(BaseModel):
    __tablename__ = 'priority_levels'
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    level: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    sla_hours: Mapped[Optional[int]] = mapped_column(Integer)
    escalation_hours: Mapped[Optional[int]] = mapped_column(Integer)
    color_code: Mapped[Optional[str]] = mapped_column(String(7))
    icon: Mapped[Optional[str]] = mapped_column(String(50))
    
    def __repr__(self) -> str:
        return f'<PriorityLevel code="{self.code}" name="{self.name}">'

class NotificationType(BaseModel):
    __tablename__ = 'notification_types'
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_email_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    is_sms_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    is_push_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    is_system_notification: Mapped[bool] = mapped_column(Boolean, default=True)
    email_template: Mapped[Optional[str]] = mapped_column(String(100))
    sms_template: Mapped[Optional[str]] = mapped_column(String(100))
    push_template: Mapped[Optional[str]] = mapped_column(String(100))
    retry_count: Mapped[int] = mapped_column(Integer, default=3)
    retry_interval_minutes: Mapped[int] = mapped_column(Integer, default=5)
    
    def __repr__(self) -> str:
        return f'<NotificationType code="{self.code}" name="{self.name}">'
    
class DeliveryType(BaseModel):
    __tablename__ = 'delivery_methods'
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    estimated_days: Mapped[Optional[int]] = mapped_column(Integer)
    cost_per_kg: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    cost_per_km: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    def __repr__(self) -> str:
        return f'<DeliveryType name="{self.name}">'
    
class ProductPrice(BaseModel):
    __tablename__ = 'product_prices'
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)
    HNA: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    HJP: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    HET: Mapped[Optional[float]] = mapped_column(Numeric(15, 2))
    
    product: Mapped['Product'] = relationship(back_populates='prices')
    sales_order_items: Mapped[List['SalesOrderItem']] = relationship(back_populates='product_price_entry')

    def __repr__(self) -> str:
        # `__repr__` yang aman, tidak memicu lazy load pada `product`.
        return f'<ProductPrice code="{self.code}" product_id={self.product_id}>'   
    
class MovementType(BaseModel):
    __tablename__ = 'movement_types'
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    ### DEVIL'S ADVOCATE NOTE ###
    # `direction` adalah kandidat sempurna untuk Enum. Ini mencegah nilai yang salah
    # seperti "in", "OUTT", atau "TRANS".
    direction: Mapped[MovementDirectionEnum] = mapped_column(SQLAlchemyEnum(MovementDirectionEnum, name="movement_direction_enum", create_type=False), nullable=False)
    
    auto_generate_document: Mapped[bool] = mapped_column(Boolean, default=False)
    document_prefix: Mapped[Optional[str]] = mapped_column(String(10))

    # Merefaktor relasi yang dikomentari ke sintaks modern.
    # stock_movements: Mapped[List['StockMovement']] = relationship(back_populates='movement_type')
    
    def __repr__(self) -> str:
        return f'<MovementType code="{self.code}" name="{self.name}">'