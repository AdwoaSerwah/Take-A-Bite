#!/usr/bin/python3
""" holds class User"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from bcrypt import gensalt, hashpw, checkpw
import secrets
from datetime import datetime, timedelta, timezone


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        username = Column(String(10), nullable=False, unique=True) # String(10)
        email = Column(String(128), nullable=False, unique=True)
        phone_number = Column(String(15), nullable=False, unique=True)
        password = Column(String(128), nullable=False)
        reset_token = Column(String(128), nullable=True)
        token_expiry = Column(DateTime, nullable=True)

        orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    else:
        first_name = ""
        last_name = ""
        username = ""
        email = ""
        phone_number = ""
        # location = ""
        password = ""

    def __init__(self, *args, **kwargs):
        """Initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """Encrypts the password with bcrypt if setting the password attribute"""
        if name == "password":
            # Use bcrypt for hashing the password with a salt
            salt = gensalt()
            value = hashpw(value.encode('utf-8'), salt).decode('utf-8')
        super().__setattr__(name, value)

    def check_password(self, password):
        """Check if the provided password matches the stored hash"""
        if self.password:
            return checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
        return False

    def generate_reset_token(self):
        """Generates the reset password token"""
        self.reset_token = secrets.token_urlsafe(64)
        self.token_expiry = datetime.now(timezone.utc) + timedelta(hours=1)  # Token valid for 1 hour
        self.save()  # Save to database

    def set_password(self, raw_password):
        """Encrypts the password using bcrypt."""
        self.password = raw_password
        self.save()  # Save the user with the new password
