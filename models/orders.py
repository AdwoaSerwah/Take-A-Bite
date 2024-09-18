#!/usr/bin/python3
"""Holds class Order"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Enum, ForeignKey, Numeric, Table
from sqlalchemy.orm import relationship
import enum

if models.storage_t == 'db':
    # Define the association table for the many-to-many relationship between orders and menu_items
    order_menu_items = Table('order_menu_items', Base.metadata,
        Column('order_id', String(60), ForeignKey('orders.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
        Column('menu_item_id', String(60), ForeignKey('menu_items.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
    )


class OrderStatus(enum.Enum):
    """Enumeration for order status"""
    PENDING = "Pending"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class Order(BaseModel, Base):
    """Representation of an order"""
    if models.storage_t == 'db':
        __tablename__ = 'orders'
        
        # Define columns specific to Order
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        total_amount = Column(Numeric(10, 2), nullable=False)
        status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
        
        # Define relationships
        user = relationship("User", back_populates="orders")
        order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
        menu_items = relationship("MenuItem", secondary=order_menu_items, back_populates="orders")
        payment = relationship("Payment", back_populates="order", uselist=False)

    else:
        # Define attributes for file storage
        user_id = ""
        total_amount = "0.00"  # Use string for file storage compatibility
        status = OrderStatus.PENDING

    def __init__(self, *args, **kwargs):
        """Initializes order"""
        super().__init__(*args, **kwargs)

    def to_dict(self):
        """Returns a dictionary representation of the order"""
        order_dict = super().to_dict()

        # Convert Enum to string for JSON serialization
        if isinstance(self.status, OrderStatus):
            order_dict['status'] = self.status.value

        # If using file storage, ensure total_amount is string (to avoid issues with numeric precision)
        if models.storage_t != 'db':
            order_dict['total_amount'] = str(self.total_amount)

        return order_dict
