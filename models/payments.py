#!/usr/bin/python3
""" holds class Payment"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Numeric, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum

class PaymentStatus(enum.Enum):
    """Enumeration for payment status"""
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"

class Payment(BaseModel, Base):
    """Representation of a payment"""
    if models.storage_t == 'db':
        __tablename__ = 'payments'
        
        # Define columns
        amount = Column(Numeric(10, 2), nullable=False)
        method = Column(String(50), nullable=False)  # e.g., Credit Card, PayPal
        status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
        order_id = Column(String(60), ForeignKey('orders.id'), nullable=False)
        transaction_ref = Column(String(255), nullable=True)
        
        # Define relationships
        order = relationship("Order", back_populates="payment")

    else:
        # Define attributes for file storage
        amount = Numeric('0.00')
        method = ""
        status = PaymentStatus.PENDING
        order_id = ""
        transaction_ref = ""

    def __init__(self, *args, **kwargs):
        """initializes payment for database"""
        super().__init__(*args, **kwargs)
