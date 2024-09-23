#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.base_model import Base, BaseModel
from models.categories import Category
from models.menu_items import MenuItem
from models.order_items import OrderItem
from models.orders import Order
from models.payments import Payment
from models.users import User
from models.locations import Location
# from models.cart_items import CartItem
# from models.carts import Cart
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# "CartItem": CartItem, "Cart": Cart
classes = {"Category": Category, "MenuItem": MenuItem, "OrderItem": OrderItem,
           "Order": Order, "Payment": Payment, "User": User, "Location": Location}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_ENV = getenv('HBNB_ENV')
        """HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))"""

        DATABASE_URL = getenv('DATABASE_URL')
        self.__engine = create_engine(DATABASE_URL)

        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None
    
    def get_by_email(self, cls, email):
        """
        Returns the object based on the class name and email, or
        None if not found.
        """
        if cls not in classes.values() or not hasattr(cls, 'email'):
            return None

        all_cls = self.all(cls)
        for value in all_cls.values():
            if getattr(value, 'email', None) == email:
                return value

        return None
    
    def get_by_username(self, cls, username):
        """
        Returns the object based on the class name and username, or
        None if not found.
        """
        if cls not in classes.values() or not hasattr(cls, 'username'):
            return None

        all_cls = self.all(cls)
        for value in all_cls.values():
            if getattr(value, 'username', None) == username:
                return value

        return None
    
    def get_by_phone(self, cls, phone):
        """
        Returns the object based on the class name and phone number, or
        None if not found.
        """
        if cls not in classes.values() or not hasattr(cls, 'phone_number'):
            return None

        all_cls = self.all(cls)
        for value in all_cls.values():
            if getattr(value, 'phone_number', None) == phone:
                return value

        return None

    def get_by_token(self, token):
        """Retrieve an object by reset_token."""
        users = self.all(User).values()
        for user in users:
            if user.reset_token == token:
                return user
        return None
    
    def get_menu_items_by_category(self, category_id):
        """Get menu items by category ID."""
        return self.__session.query(MenuItem).filter_by(category_id=category_id).all()

    def get_menu_items_by_name(self, name):
        """Get menu items by name."""
        return self.__session.query(MenuItem).filter(MenuItem.name.ilike(f'%{name}%')).all()

    def get_all_menu_items(self):
        """Get all menu items."""
        return self.__session.query(MenuItem).all()
    
    def get_all_categories(self):
        """Get all categories."""
        return self.__session.query(Category).all()

    def get_pending_order_by_user(self, user_id):
        """Fetches the pending order for a given user, if any."""
        session = self.__session
        try:
            pending_order = session.query(Order).filter(
                Order.user_id == user_id,
                Order.status == "PENDING"  # Or whatever status represents pending orders
            ).one_or_none()
            return pending_order
        except Exception as e:
            print(f"Error fetching pending order: {e}")
            return None
        
        
    def calculate_order_total(self, order_id):
        """Calculate the total amount for a given order."""
        try:
            order_items = self.__session.query(OrderItem).filter_by(order_id=order_id).all()
            total = sum(item.price for item in order_items)
            return total
        except Exception as e:
            print(f"Error calculating order total: {e}")
            return 0


    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count

    
    def get_payment_by_order(self, order_id):
        """Fetch payment details for a given order_id."""
        try:
            payment = self.__session.query(Payment).filter_by(order_id=order_id).first()
            return payment
        except Exception as e:
            print(f"Error fetching payment by order: {e}")
            return None
        
    def get_order_by_id(self, order_id):
        """Retrieve an order by its ID."""
        try:
            order = self.__session.query(Order).filter_by(id=order_id).one_or_none()
            return order
        except Exception as e:
            print(f"Error fetching order by ID: {e}")
            return None

