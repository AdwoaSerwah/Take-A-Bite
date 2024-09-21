#!/usr/bin/python3
""" holds class Location"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Numeric
from sqlalchemy.orm import relationship


class Location(BaseModel, Base):
    """Representation of a location"""
    if models.storage_t == 'db':
        __tablename__ = 'locations'

        name = Column(String(128), nullable=False)
        delivery_price = Column(Numeric(10, 2), nullable=False)

        # Relationship
        orders = relationship("Order", back_populates="location")
    else:
        name = ""
        delivery_price = Numeric('0.00')

    def __init__(self, *args, **kwargs):
        """initializes menu item"""
        super().__init__(*args, **kwargs)
