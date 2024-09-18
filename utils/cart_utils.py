#!/usr/bin/python3
""" Cart helper functions """
from models import storage
from models.users import User
from flask import session


def get_user_and_cart_info():
    """ Get user and cart information """
    user_id = session.get('user_id')
    user = storage.get(User, user_id) if user_id else None
    username = user.username if user else None
    
    cart_items = {}
    if user_id:
        order = storage.get_pending_order_by_user(user_id)
        if order:
            cart_items = {item.menu_item_id: item.quantity for item in order.order_items}
            cart_item_count = sum(cart_items.values())
        else:
            cart_item_count = 0
    else:
        cart_item_count = 0

    return user, username, cart_item_count, cart_items
