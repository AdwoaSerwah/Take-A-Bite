#!/usr/bin/python3
""" Blueprint for HTML views """
from flask import render_template, session, redirect, url_for, request
from api.v1.views import html_views
import uuid
from models.users import User
from models import storage
# from models.categories import Category
from api.v1.views.auth import check_authentication
# from flask import Flask, make_response, jsonify, request
from utils.cart_utils import get_user_and_cart_info
from models.menu_items import MenuItem
from models.locations import Location
# from utils.email_utils import send_password_reset_email 


@html_views.route('/signup/', methods=['GET', 'POST'], strict_slashes=False)
def signup():
    """ Sign up template rendering """
    cache_id = uuid.uuid4()
    return render_template('signup.html', cache_id=cache_id)


@html_views.route('/login/', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """ Login template rendering """
    cache_id = uuid.uuid4()
    return render_template('login.html', cache_id=cache_id)


@html_views.route('/account_management/', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
@check_authentication
def account_management():
    """Account management template rendering"""
    user_id = session.get('user_id')  # Get the current user ID from the session
    user = storage.get(User, user_id)  # Retrieve user details from the database
    
    if user:
        cache_id = uuid.uuid4()
        return render_template('account_management.html', user=user, cache_id=cache_id)


"""@html_views.route('/logout/', methods=['GET', 'POST'], strict_slashes=False)
def logout():
    Logout template rendering
    cache_id = uuid.uuid4()
    return render_template('logout.html', cache_id=cache_id)"""


@html_views.route('/forgot_password/', methods=['GET', 'POST'], strict_slashes=False)
def forgot_password():
    """ Forgot password template rendering """
    cache_id = uuid.uuid4()
    return render_template('forgot_password.html', cache_id=cache_id)


@html_views.route('/reset_password/<token>', methods=['GET', 'POST'], strict_slashes=False)
def reset_password(token):
    """ Reset password template rendering """
    cache_id = uuid.uuid4()
    return render_template('reset_password.html', cache_id=cache_id, token=token)


@html_views.route('/check_email/', methods=['GET'], strict_slashes=False)
def check_email():
    """ Render check email page """
    cache_id = uuid.uuid4()
    return render_template('check_email.html', cache_id=cache_id)


@html_views.route('/', strict_slashes=False)
@html_views.route('/home/', strict_slashes=False)
def home():
    """ Index template rendering """
    cache_id = uuid.uuid4()
    return render_template('index.html', cache_id=cache_id)


@html_views.route('/about/', strict_slashes=False)
def about():
    """ About template rendering """
    cache_id = uuid.uuid4()
    return render_template('about.html', cache_id=cache_id)


@html_views.route('/contact/', strict_slashes=False)
def contact():
    """ Contact template rendering """
    cache_id = uuid.uuid4()
    return render_template('contact.html', cache_id=cache_id)


@html_views.route('/menu/', strict_slashes=False)
def menu():
    """Menu template rendering with filtering and searching."""
    cache_id = uuid.uuid4()

    # Use the helper function to get user and cart information
    user, username, cart_item_count, cart_items = get_user_and_cart_info()
    menu_items = storage.get_all_menu_items()  
    categories = storage.get_all_categories() 

    print("Cart-counter: ", cart_item_count)
    
    return render_template('menu.html',
                           cache_id=cache_id,
                           user=user,
                           username=username,
                           menu_items=menu_items,
                           categories=categories,
                           cart_item_count=cart_item_count,
                           cart_items=cart_items)




"""@html_views.route('/cart/', strict_slashes=False)
@check_authentication
def cart():
    Cart template rendering
    cache_id = uuid.uuid4()
    # Use the helper function to get user and cart information
    user, username, cart_item_count, cart_items = get_user_and_cart_info()
    menu_items = storage.get_all_menu_items()

    return render_template('cart.html', 
                           cache_id=cache_id, 
                           user=user, 
                           username=username, 
                           menu_items=menu_items,
                           cart_item_count=cart_item_count,
                           cart_items=cart_items)"""


@html_views.route('/cart/', strict_slashes=False)
@check_authentication
def cart():
    """Cart template rendering"""
    cache_id = uuid.uuid4()

    # Use the helper function to get user and cart information
    user, username, cart_item_count, cart_items = get_user_and_cart_info()

    # Ensure cart_items contains more information than just quantity (fetch MenuItem details)
    enriched_cart_items = []
    cart_subtotal = 0
    for menu_item_id, quantity in cart_items.items():
        menu_item = storage.get(MenuItem, menu_item_id)
        if menu_item:
            total_price = menu_item.price * quantity
            cart_subtotal += total_price
            enriched_cart_items.append({
                'menu_item': menu_item,
                'quantity': quantity,
                'total_price': total_price
            })

    # Fetch available locations for delivery options
    locations = storage.all(Location)

    # Render the cart.html template with the enriched cart data and location info
    return render_template('cart.html', 
                           cache_id=cache_id, 
                           user=user, 
                           username=username, 
                           cart_item_count=cart_item_count,
                           cart_items=enriched_cart_items,
                           cart_subtotal=cart_subtotal,
                           locations=locations.values())


#@html_views.route('/cart/', strict_slashes=False)
#@check_authentication
#def cart():
    """ Cart template rendering
    cache_id = uuid.uuid4()

    # Use the helper function to get user and cart information
    user, username, cart_item_count, cart_items = get_user_and_cart_info()

    # Ensure cart_items contains more information than just quantity (fetch MenuItem details)
    enriched_cart_items = []
    cart_subtotal = 0
    for menu_item_id, quantity in cart_items.items():
        menu_item = storage.get(MenuItem, menu_item_id)
        if menu_item:
            total_price = menu_item.price * quantity
            cart_subtotal += total_price
            enriched_cart_items.append({
                'menu_item': menu_item,
                'quantity': quantity,
                'total_price': total_price
            })

    # Render the cart.html template with the enriched cart data
    return render_template('cart.html', 
                           cache_id=cache_id, 
                           user=user, 
                           username=username, 
                           cart_item_count=cart_item_count,
                           cart_items=enriched_cart_items,
                           cart_subtotal=cart_subtotal)
 """


#@html_views.route('/cart/', strict_slashes=False)
#@check_authentication
#def cart():
    """ Cart template rendering with delivery or pickup option
    cache_id = uuid.uuid4()

    # Use the helper function to get user and cart information
    user, username, cart_item_count, cart_items = get_user_and_cart_info()

    # Get all locations and their delivery prices
    locations = storage.get_all_locations()

    cart_subtotal = sum(item.quantity * item.menu_item.price for item in cart_items.values())
    
    return render_template('cart.html', 
                           cache_id=cache_id, 
                           user=user, 
                           username=username, 
                           cart_item_count=cart_item_count,
                           cart_items=cart_items,
                           cart_subtotal=cart_subtotal,
                           locations=locations)
 """
