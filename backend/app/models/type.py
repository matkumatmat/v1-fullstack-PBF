import uuid
from sqlalchemy import(
    Column, Integer, String, ForeignKey, 
    Text, DateTime, Date, Numeric, Boolean,
    Float, func, UniqueConstraint, Table
)
from sqlalchemy.orm import relationship
from .base import BaseModel

# Tabel perantara untuk SalesOrderItem <-> SectorType
sales_order_item_sector_association = Table(
    'so_item_sector_association',
    BaseModel.metadata,
    Column('sales_order_item_id', Integer, ForeignKey('sales_order_items.id'), primary_key=True),
    Column('sector_type_id', Integer, ForeignKey('sector_types.id'), primary_key=True)
)

# Tabel perantara untuk SalesOrderItem <-> AllocationType
sales_order_item_allocation_association = Table(
    'so_item_allocation_association',
    BaseModel.metadata,
    Column('sales_order_item_id', Integer, ForeignKey('sales_order_items.id'), primary_key=True),
    Column('allocation_type_id', Integer, ForeignKey('allocation_types.id'), primary_key=True)
)

#===PRODUCT ENUMS===#   
class ProductType(BaseModel):
    """Master data untuk jenis produk"""
    __tablename__ = 'product_types'
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    sort_order = Column(Integer, default=0)

    products = relationship('Product', back_populates='product_type')
    def __repr__(self):
        return f'<ProductType {self.code}: {self.name}>'
    
class PackageType(BaseModel):
    __tablename__ = 'package_types'
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    is_fragile = Column(Boolean, default=False, nullable=False)
    is_stackable = Column(Boolean, default=True, nullable=False)
    max_stack_height = Column(Integer, nullable=True)
    special_handling_required = Column(Boolean, default=False)
    handling_instructions = Column(Text)

    products = relationship('Product', back_populates='package_type')
    def __repr__(self):
        return f'<PackageType {self.code}: {self.name}>'    

class TemperatureType(BaseModel):
    __tablename__ = 'temperature_types'
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    min_celsius = Column(Float)
    max_celsius = Column(Float)
    optimal_celsius = Column(Float)
    celsius_display = Column(String(20))  # e.g., "2-8°C", "-18°C"
    humidity_range = Column(String(20))  # e.g., "45-75%"
    special_storage_requirements = Column(Text)

    color_code = Column(String(7))  # Hex color untuk UI
    icon = Column(String(50))  # Icon name untuk UI
    
    # Relationships
    products = relationship('Product', back_populates='temperature_type')
    warehouses = relationship('Warehouse', back_populates='temperature_type')
    
    def __repr__(self):
        return f'<TemperatureType {self.code}: {self.name}>'

class AllocationType(BaseModel):
    __tablename__ = 'allocation_types'
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)

    color_code = Column(String(7))  # Hex color
    icon = Column(String(50))

    allocations = relationship('Allocation', back_populates='allocation_type')
    sales_order_items = relationship(
        'SalesOrderItem',
        secondary=sales_order_item_allocation_association,
        back_populates='allocations'
    )    
    
    def __repr__(self):
        return f'<AllocationType {self.code}: {self.name}>'
    
class SectorType(BaseModel):
    __tablename__ = 'sector_types'
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False)

    requires_special_handling = Column(Boolean, default=False)
    default_payment_terms = Column(Integer)  # Days
    default_delivery_terms = Column(String(50))
    
    requires_temperature_monitoring = Column(Boolean, default=False)
    requires_chain_of_custody = Column(Boolean, default=False)
    special_documentation = Column(Text)
    
    customers = relationship('Customer', back_populates='sector_type')
    sales_order_items = relationship(
        'SalesOrderItem',
        secondary=sales_order_item_sector_association,
        back_populates='sectors'
    )    
    
    def __repr__(self):
        return f'<SectorType {self.code}: {self.name}>'
        
class CustomerType(BaseModel):
    __tablename__ = 'customer_types'
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False)
    allows_tender_allocation = Column(Boolean, default=False)
    requires_pre_approval = Column(Boolean, default=False)
    default_credit_limit = Column(Numeric(15, 2))
    default_discount_percent = Column(Numeric(5, 2))
    default_payment_terms_days = Column(Integer, default=30)
    
    customers = relationship('Customer', back_populates='customer_type')
    
    def __repr__(self):
        return f'<CustomerType {self.code}: {self.name}>'

class DocumentType(BaseModel):
    __tablename__ = 'document_types'
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False)

    is_mandatory = Column(Boolean, default=False)
    is_customer_visible = Column(Boolean, default=True)
    max_file_size_mb = Column(Integer, default=10)
    allowed_extensions = Column(String(100))  # e.g., "pdf,jpg,png"

    auto_generate = Column(Boolean, default=False)
    template_path = Column(String(255))
    #shipment_documents = relationship('ShipmentDocument', back_populates='document_type')
    
    def __repr__(self):
        return f'<DocumentType {self.code}: {self.name}>'

class StatusType(BaseModel):
    __tablename__ = 'status_types'
    entity_type = Column(String(50), nullable=False, index=True)  # SO, SHIPMENT, PICKING, etc
    code = Column(String(20), nullable=False, index=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False)

    is_initial_status = Column(Boolean, default=False)
    is_final_status = Column(Boolean, default=False)
    is_error_status = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    
    # UI properties
    color_code = Column(String(7))  # Hex color
    icon = Column(String(50))
    css_class = Column(String(50))

    auto_transition_after_hours = Column(Integer)  # Auto transition setelah X jam
    requires_approval = Column(Boolean, default=False)
    sends_notification = Column(Boolean, default=False)
    
    __table_args__ = (
        UniqueConstraint('entity_type', 'code', name='uq_status_entity_code'),
    )
    
    def __repr__(self):
        return f'<StatusType {self.entity_type}.{self.code}: {self.name}>'

class LocationType(BaseModel):
    __tablename__ = 'location_types'
    
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Location properties
    is_storage_location = Column(Boolean, default=True)
    is_picking_location = Column(Boolean, default=True)
    is_staging_location = Column(Boolean, default=False)
    
    max_weight_capacity_kg = Column(Float)
    supports_temperature_control = Column(Boolean, default=False)
    requires_special_access = Column(Boolean, default=False)
    
    def __repr__(self):
        return f'<LocationType {self.code}: {self.name}>'

class PackagingMaterial(BaseModel):
    __tablename__ = 'packaging_materials'
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False)

    material_type = Column(String(20))  # BOX, BUBBLE_WRAP, TAPE, etc
    is_reusable = Column(Boolean, default=False)
    is_fragile_protection = Column(Boolean, default=False)
    is_temperature_protection = Column(Boolean, default=False)

    length_cm = Column(Float)
    width_cm = Column(Float)
    height_cm = Column(Float)
    weight_g = Column(Float)

    cost_per_unit = Column(Numeric(8, 2))
    
    def __repr__(self):
        return f'<PackagingMaterial {self.code}: {self.name}>'
    
class PackagingBoxType(BaseModel):
    __tablename__ = 'packaging_box_types'
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False)
    material_type = Column(String(20))  # PU1, CKS, PU2, 
    is_reusable = Column(Boolean, default=False)
    is_fragile_protection = Column(Boolean, default=False)
    is_temperature_protection = Column(Boolean, default=False)

    length_cm = Column(Float)
    width_cm = Column(Float)
    height_cm = Column(Float)
    weight_g = Column(Float)

    cost_per_unit = Column(Numeric(8, 2))
    
    def __repr__(self):
        return f'<PackagingBoxtype {self.code}: {self.name}>'    

class PriorityLevel(BaseModel):
    """Master data untuk tingkat prioritas"""
    __tablename__ = 'priority_levels'
    
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Priority properties
    level = Column(Integer, unique=True, nullable=False)  # 1=highest, 9=lowest
    sla_hours = Column(Integer)  # SLA dalam jam
    escalation_hours = Column(Integer)  # Escalate setelah X jam
    
    # UI properties
    color_code = Column(String(7))
    icon = Column(String(50))
    
    def __repr__(self):
        return f'<PriorityLevel {self.code}: {self.name}>'

class NotificationType(BaseModel):
    __tablename__ = 'notification_types'
    
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Notification properties
    is_email_enabled = Column(Boolean, default=True)
    is_sms_enabled = Column(Boolean, default=False)
    is_push_enabled = Column(Boolean, default=True)
    is_system_notification = Column(Boolean, default=True)
    
    # Template properties
    email_template = Column(String(100))
    sms_template = Column(String(100))
    push_template = Column(String(100))
    
    # Delivery rules
    retry_count = Column(Integer, default=3)
    retry_interval_minutes = Column(Integer, default=5)
    
    def __repr__(self):
        return f'<NotificationType {self.code}: {self.name}>'
    
class DeliveryType(BaseModel):
    """Master data untuk metode pengiriman"""
    __tablename__ = 'delivery_methods'
    
    name = Column(String(100), unique=True, nullable=False)  # Express, Regular, Economy
    description = Column(Text)
    estimated_days = Column(Integer)  # Estimasi hari pengiriman
    cost_per_kg = Column(Numeric(10, 2))
    cost_per_km = Column(Numeric(10, 2))
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f'<DeliveryMethod {self.name}>'
    
class ProductPrice(BaseModel):
    __tablename__ = 'product_prices'

    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100))
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    effective_date = Column(Date, nullable=False)
    HNA = Column(Numeric(15, 2))
    HJP = Column(Numeric(15, 2))
    HET = Column(Numeric(15, 2))
    
    product = relationship('Product', back_populates='prices')
    sales_order_items = relationship('SalesOrderItem', back_populates='product_price_entry')

    def __repr__(self):
        return f'<ProductPrice {self.code} for {self.product.name}>'   
    
class MovementType(BaseModel):
    __tablename__ = 'movement_types'
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    direction = Column(String(10), nullable=False)  # IN, OUT, TRANSFER
    auto_generate_document = Column(Boolean, default=False)
    document_prefix = Column(String(10))

    #stock_movements = relationship('StockMovement', back_populates='movement_type')
    
    def __repr__(self):
        return f'<MovementType {self.code}: {self.name}>'
