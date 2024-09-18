#!/usr/bin/python3
""" holds class OrderItem"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship

class OrderItem(BaseModel, Base):
    """Representation of an order item"""
    if models.storage_t == 'db':
        __tablename__ = 'order_items'

        # Define columns specific to OrderItem
        order_id = Column(String(60), ForeignKey('orders.id'), nullable=False)
        menu_item_id = Column(String(60), ForeignKey('menu_items.id'), nullable=False)
        quantity = Column(Integer, nullable=False, default=1)
        price = Column(Numeric(10, 2), nullable=False)

        # Define relationships
        order = relationship("Order", back_populates="order_items")
        menu_item = relationship("MenuItem", back_populates="order_items")
    else:
        # Define attributes for file storage
        order_id = ""
        menu_item_id = ""
        quantity = 1
        price = Numeric('0.00')

    def __init__(self, *args, **kwargs):
        """initializes order item for database"""
        super().__init__(*args, **kwargs)
