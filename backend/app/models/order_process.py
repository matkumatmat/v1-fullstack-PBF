import uuid
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Text, DateTime, Date, Numeric, Boolean,
    func, Table
)
from sqlalchemy.orm import relationship
from .newmodels.base import BaseModel
from .type import (
    SectorType, AllocationType,
    sales_order_item_sector_association,
    sales_order_item_allocation_association
)


class SalesOrder(BaseModel):
    __tablename__ = 'sales_order'
    public_id = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False, index=True)
    so_number = Column(String(50), nullable=False, index=True)
    #customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    #customer = relationship('Customer', back_populates='sales_orders')
    so_date = Column(Date, nullable=False)
    total_amount = Column(Numeric(15, 2))
    status = Column(String(50), default='PENDING', nullable=False)  
    input_by = Column(String(50))  
    notes = Column(Text)
    special_instructions = Column(Text)
    items = relationship('SalesOrderItem', back_populates='sales_order', cascade='all, delete-orphan')
    #shipping_plan = relationship('ShippingPlan', back_populates='sales_order')
    #tender_contract_id = Column(Integer, ForeignKey('tender_contracts.id'), nullable=True)
    #tender_contract = relationship('TenderContract', back_populates='sales_order')
    #packing_orders = relationship('PackingOrder', back_populates='sales_order')
    is_tender_so = Column(Boolean, default=False)
    @property
    def so_type(self):
        return 'TENDER' if self.is_tender_so else 'REGULAR'    
    
    @property
    def total_quantity_requested(self):
        """Total quantity dari semua items dalam SO"""
        return sum(item.quantity_requested for item in self.items)
    
    @property
    def total_quantity_planned(self):
        """Total quantity yang sudah masuk shipping plan"""
        total = 0
        for item in self.items:
            total += sum(spi.quantity_to_fulfill for spi in item.shipping_plan_items)
        return total
    
    @property
    def is_fully_planned(self):
        """Apakah SO sudah fully planned"""
        return self.total_quantity_planned >= self.total_quantity_requested
    
    def __repr__(self):
        return f'<SalesOrder {self.so_number}>'

class SalesOrderItem(BaseModel):
    __tablename__ = 'sales_order_items'
    
    line_number = Column(Integer)
    quantity_requested = Column(Integer, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    total_price = Column(Numeric(15, 2))
    #product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    sales_order_id = Column(Integer, ForeignKey('sales_order.id'), nullable=False)
    required_delivery_date = Column(Date)
    status = Column(String(50), default='PENDING')
    price_type_code_used = Column(String(20), nullable=False)
    #product_price_id = Column(Integer, ForeignKey('product_prices.id'), nullable=True)

    #product = relationship('Product', back_populates='sales_order_items')
    sales_order = relationship('SalesOrder', back_populates='items')
    #product_price_entry = relationship('ProductPrice', back_populates='sales_order_items')
    shipping_plan_items = relationship('ShippingPlanItem', back_populates='sales_order_item', cascade='all, delete-orphan')
    
    sectors = relationship(
        'SectorType',
        secondary=sales_order_item_sector_association,
        back_populates='sales_order_items'
    )
    
    allocations = relationship(
        'AllocationType',
        secondary=sales_order_item_allocation_association,
        back_populates='sales_order_items'
    )
    
    @property
    def quantity_planned(self):
        return sum(spi.quantity_to_fulfill for spi in self.shipping_plan_items)
    
    @property
    def quantity_remaining(self):
        return self.quantity_requested - self.quantity_planned
    
    @property
    def is_fully_planned(self):
        return self.quantity_planned >= self.quantity_requested
    
    def __repr__(self):
        return f'<SalesOrderItem {self.sales_order.so_number}-{self.line_number}>'

class ShippingPlan(BaseModel):
    __tablename__ = 'shipping_plan'
    public_id = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False, index=True)
    plan_number = Column(String(50), unique=True, nullable=False, index=True)
    planned_delivery_date = Column(Date, nullable=False)
    actual_delivery_date = Column(Date)
    #sales_order_id = Column(Integer, ForeignKey('sales_order.id'), nullable=False)
    #sales_order = relationship('SalesOrder', back_populates='shipping_plan')
    shipping_method = Column(String(50))  
    status = Column(String(50), default='PENDING', nullable=False)

    created_by = Column(String(50))  # Tim penjualan yang buat plan
    created_date = Column(DateTime, default=func.current_timestamp())
    confirmed_by = Column(String(50))
    confirmed_date = Column(DateTime)
    delivery_address = Column(Text)
    contact_person = Column(String(100))
    contact_phone = Column(String(20))

    items = relationship('ShippingPlanItem', back_populates='shipping_plan', cascade='all, delete-orphan')
    #picking_lists = relationship('PickingList', back_populates='shipping_plan')
    #shipment = relationship('Shipment', back_populates='shipping_plan', uselist=False)

    @property
    def total_quantity(self):
        """Total quantity dalam shipping plan"""
        return sum(item.quantity_to_fulfill for item in self.items)
    
    @property
    def total_products(self):
        """Total jenis produk dalam shipping plan"""
        return len(self.items)
    
    @property
    def has_picking_list(self):
        """Apakah sudah ada picking list"""
        return len(self.picking_lists) > 0
    
    def __repr__(self):
        return f'<ShippingPlan {self.plan_number}>'

class ShippingPlanItem(BaseModel):
    __tablename__ = 'shipping_plan_items'
    quantity_to_fulfill = Column(Integer, nullable=False)
    shipping_plan_id = Column(Integer, ForeignKey('shipping_plan.id'), nullable=False)
    shipping_plan = relationship('ShippingPlan', back_populates='items')
    sales_order_item_id = Column(Integer, ForeignKey('sales_order_items.id'), nullable=False)
    sales_order_item = relationship('SalesOrderItem', back_populates='shipping_plan_items')
    line_number = Column(Integer) 
    planned_date = Column(Date)
    status = Column(String(50), default='PENDING') 
    #picking_list_items = relationship('PickingListItem', back_populates='shipping_plan_item')
    @property
    def product(self):
        """Get product dari SO item"""
        return self.sales_order_item.product if self.sales_order_item else None
    
    @property
    def sales_order(self):
        """Get sales order dari SO item"""
        return self.sales_order_item.sales_order if self.sales_order_item else None
    
    @property
    def customer(self):
        """Get customer dari shipping plan"""
        return self.shipping_plan.customer if self.shipping_plan else None
    
    @property
    def is_picking_list_created(self):
        """Apakah sudah ada picking list untuk item ini"""
        return len(self.picking_list_items) > 0
    
    def __repr__(self):
        return f'<ShippingPlanItem {self.shipping_plan.plan_number}-{self.line_number}>'
    

 