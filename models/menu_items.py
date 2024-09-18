#!/usr/bin/python3
""" holds class MenuItem"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from models.orders import order_menu_items


class MenuItem(BaseModel, Base):
    """Representation of a menu item"""
    if models.storage_t == 'db':
        __tablename__ = 'menu_items'
        name = Column(String(128), nullable=False)
        description = Column(String(256), nullable=True)
        price = Column(Numeric(10, 2), nullable=False)
        category_id = Column(String(60), ForeignKey('categories.id'), nullable=False)
        image_url = Column(String(256), nullable=True)

        category = relationship("Category", back_populates="menu_items")
        orders = relationship("Order", secondary=order_menu_items, back_populates="menu_items")
        order_items = relationship("OrderItem", back_populates="menu_item")
        # cart_items = relationship("CartItem", back_populates="menu_item", cascade="all, delete-orphan")

    else:
        name = ""
        description = ""
        price = Numeric('0.00')
        category_id = ""

    def __init__(self, *args, **kwargs):
        """initializes menu item"""
        super().__init__(*args, **kwargs)
