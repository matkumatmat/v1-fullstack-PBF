import uuid
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Text, DateTime, Float,
    func
)
from sqlalchemy.orm import relationship
from .base import BaseModel

class PickingList(BaseModel):
    __tablename__ = 'picking_lists'
    public_id = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False, index=True)
    picking_list_number = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(String(50), default='PENDING', nullable=False) 
    created_by = Column(String(50))  
    shipping_plan_id = Column(Integer, ForeignKey('shipping_plans.id'), nullable=False)
    shipping_plan = relationship('ShippingPlan', back_populates='picking_lists')
    items = relationship('PickingListItem', back_populates='picking_list', cascade='all, delete-orphan')
    picking_orders = relationship('PickingOrder', back_populates='picking_list')
    packing_slip_id = Column(Integer, ForeignKey('packing_slips.id'), nullable=True)
    packing_slip = relationship('PackingSlip', back_populates='picking_lists')

class PickingListItem(BaseModel):
    __tablename__ = 'picking_list_items'
    quantity_to_pick = Column(Integer, nullable=False)
    allocation_id = Column(Integer, ForeignKey('allocations.id'), nullable=False)
    allocation = relationship('Allocation')
    rack_id = Column(Integer, ForeignKey('racks.id'), nullable=False)
    rack = relationship('Rack')
    shipping_plan_item_id = Column(Integer, ForeignKey('shipping_plan_items.id'), nullable=False)
    shipping_plan_item = relationship('ShippingPlanItem')
    picking_list_id = Column(Integer, ForeignKey('picking_lists.id'), nullable=False)
    picking_list = relationship('PickingList', back_populates='items')
    
    @property
    def product(self):
        return self.allocation.batch.product if self.allocation and self.allocation.batch else None
    @property
    def batch(self):
        return self.allocation.batch if self.allocation else None
    @property
    def customer(self):
        return self.allocation.customer if self.allocation else None

class PickingOrder(BaseModel):
    """Model untuk Picking Order yang dieksekusi oleh tim gudang"""
    __tablename__ = 'picking_orders'

    public_id = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False, index=True)
    picking_order_number = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(String(50), default='PENDING', nullable=False)  # PENDING, IN_PROGRESS, COMPLETED, CANCELLED

    picking_list_id = Column(Integer, ForeignKey('picking_lists.id'), nullable=False)
    picking_list = relationship('PickingList', back_populates='picking_orders')
    shipment_id = Column(Integer, ForeignKey('shipments.id'), nullable=True)
    shipment = relationship('Shipment', back_populates='picking_orders')

    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    picked_by = Column(String(50))  
    items = relationship('PickingOrderItem', back_populates='picking_order', cascade='all, delete-orphan')
    packing_orders = relationship('PackingOrder', back_populates='picking_order')

class PickingOrderItem(BaseModel):
    __tablename__ = 'picking_order_items'
    quantity_requested = Column(Integer, nullable=False)
    quantity_picked = Column(Integer, default=0, nullable=False)    
    allocation_id = Column(Integer, ForeignKey('allocations.id'), nullable=False)
    allocation = relationship('Allocation')
    rack_id = Column(Integer, ForeignKey('racks.id'), nullable=False)
    rack = relationship('Rack')
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship('Product')
    picking_list_item_id = Column(Integer, ForeignKey('picking_list_items.id'), nullable=True)
    picking_list_item = relationship('PickingListItem')
    scanned_at = Column(DateTime)
    scanned_by = Column(String(50))
    status = Column(String(50), default='PENDING') 
    notes = Column(Text)  
    picking_order_id = Column(Integer, ForeignKey('picking_orders.id'), nullable=False)
    picking_order = relationship('PickingOrder', back_populates='items')

    @property
    def batch(self):
        return self.allocation.batch if self.allocation else None
    
    @property
    def customer(self):
        return self.allocation.customer if self.allocation else None
