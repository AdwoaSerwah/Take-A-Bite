#!/usr/bin/python3
""" holds class Category"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class Category(BaseModel, Base):
    """Representation of a category"""
    if models.storage_t == 'db':
        __tablename__ = 'categories'
        name = Column(String(128), nullable=False, unique=True)

        menu_items = relationship("MenuItem", back_populates="category")
    else:
        # Define attributes for file storage
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes category for database"""
        super().__init__(*args, **kwargs)
