import uuid
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Text, DateTime, Date, Numeric, Boolean,
    Float, func
)
from sqlalchemy.orm import relationship
from .base import BaseModel

class PackingOrder(BaseModel):
    __tablename__ = 'packing_orders'
    public_id = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False, index=True)
    packing_order_number = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(String(50), default='PENDING', nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    customer = relationship('Customer')
    sales_order_id = Column(Integer, ForeignKey('sales_order.id'), nullable=False)
    sales_order = relationship('SalesOrder', back_populates='packing_orders')
    picking_order_id = Column(Integer, ForeignKey('picking_orders.id'), nullable=False)
    picking_order = relationship('PickingOrder', back_populates='packing_orders')
    created_by = Column(String(50))  # Tim packing
    completed_at = Column(DateTime)
    boxes = relationship('PackingBox', back_populates='packing_order', cascade='all, delete-orphan')

class PackingBox(BaseModel):
    __tablename__ = 'packing_boxes'
    box_number = Column(String(50), nullable=False)  # Box 1, Box 2, dst
    box_type = Column(String(50))  # Jenis box yang digunakan
    total_weight = Column(Float)
    notes = Column(Text)
    packing_order_id = Column(Integer, ForeignKey('packing_orders.id'), nullable=False)
    packing_order = relationship('PackingOrder', back_populates='boxes')
    packaging_material_id = Column(Integer, ForeignKey('packaging_materials.id'), nullable=True)
    packaging_material = relationship('PackagingMaterial')  
    Packaging_box_type_id = Column(Integer, ForeignKey('Packaging_box_types.id'), nullable=False)  
    packaging_box_type = relationship('PackagingBoxType')
    
    items = relationship('PackingBoxItem', back_populates='box', cascade='all, delete-orphan')

class PackingBoxItem(BaseModel):
    __tablename__ = 'packing_box_items'
    quantity_packed = Column(Integer, nullable=False)
    box_id = Column(Integer, ForeignKey('packing_boxes.id'), nullable=False)
    box = relationship('PackingBox', back_populates='items')
    picking_order_item_id = Column(Integer, ForeignKey('picking_order_items.id'), nullable=False)
    picking_order_item = relationship('PickingOrderItem')

    @property
    def product(self):
        return self.picking_order_item.product if self.picking_order_item else None
    
    @property
    def batch(self):
        return self.picking_order_item.batch if self.picking_order_item else None
    
    @property
    def allocation(self):
        return self.picking_order_item.allocation if self.picking_order_item else None