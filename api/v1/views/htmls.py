#!/usr/bin/python3
""" Blueprint for HTML views """
from flask import render_template, session, make_response, request
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
from models.orders import Order
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
    locations = {loc.id: loc for loc in storage.all(Location).values()}  # Ensure we're getting Location objects
    print("Locations: ", locations)

    # Define pickup_id based on the pickup location
    pickup_id = next((loc.id for loc in locations.values() if loc.name == "Pickup"), None)
    print("pickup id: ", pickup_id)

    # Retrieve the user's pending order or None if no order exists
    existing_order = storage.get_pending_order_by_user(user.id)

    # Initialize selected_location and delivery_fee
    selected_location = "Pickup"
    delivery_fee = 0

    if existing_order and existing_order.location:
        selected_location = existing_order.location.name
        delivery_fee = existing_order.location.delivery_price  # Get delivery price

    # Check for existing pending payment based on the order ID
    existing_payment = storage.get_payment_by_order(existing_order.id) if existing_order else None
    payment_method = existing_payment.method if existing_payment else 'Cash'

    print('Payment method: ', payment_method)
    

    # Render the cart.html template
    response = make_response(render_template('cart.html',
                           cache_id=cache_id,
                           user=user,
                           username=username,
                           cart_item_count=cart_item_count,
                           cart_items=enriched_cart_items,
                           cart_subtotal=cart_subtotal,
                           locations=locations,  # Use locations as dict for easier lookup in template
                           selected_location=selected_location,
                           existing_order=existing_order,  # Ensure this is passed                           
                           pickup_id=pickup_id,
                           payment_method=payment_method,
                           delivery_fee=delivery_fee))

    # Adding no-cache headers to ensure the page doesn't get cached
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response


@html_views.route('/checkout/', methods=['GET'], strict_slashes=False)
@check_authentication
def checkout():
    cache_id = uuid.uuid4()  # Generate a unique cache ID

    # Retrieve user and cart information
    user, username, cart_item_count, _ = get_user_and_cart_info()

    # Retrieve the user's pending order
    existing_order = storage.get_pending_order_by_user(user.id)

    # Retrieve payment method and details from the payments table
    payment = storage.get_payment_by_order(existing_order.id) if existing_order else None
    selected_payment_method = payment.method if payment else 'Cash'
    total_amount = payment.amount if payment else 0

    print('Selected Payment method: ', selected_payment_method)
    
    # Initialize selected_location and delivery_fee
    location = "Pickup"
    delivery_price = 0


    # Retrieve location and delivery price
    if existing_order and existing_order.location:
        location = existing_order.location.name if existing_order.location else "Pickup"
        delivery_price = existing_order.location.delivery_price if existing_order.location else 0

    # Calculate subtotal using total_amount and delivery_price
    subtotal = total_amount - delivery_price

    # Render the checkout template with no-cache headers
    response = make_response(render_template('checkout.html',
                                             selected_payment_method=selected_payment_method,
                                             existing_order=existing_order,
                                             user=user,
                                             username=username,
                                             cart_item_count=cart_item_count,
                                             cache_id=cache_id,
                                             location=location,
                                             delivery_price=delivery_price,
                                             subtotal=subtotal,
                                             total_amount=total_amount))
    
    # Adding no-cache headers to ensure the page doesn't get cached
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response


@html_views.route('/order-status/<string:order_id>', methods=['GET'], strict_slashes=False)
@check_authentication
def order_status(order_id):
    """Render the order status page."""
    cache_id = uuid.uuid4()  # Generate a unique cache ID
    user, username, cart_item_count, cart_items = get_user_and_cart_info()

    # Retrieve the order by ID
    order = storage.get_order_by_id(order_id)
    
    if not order or order.user_id != user.id:
        return make_response(render_template('404.html'), 404)  # Handle order not found
    
    # Convert order to dictionary
    order_dict = order.to_dict()


    # Retrieve payment details
    payment = storage.get_payment_by_order(order.id)
    print('Order dict: ', order_dict)
    
    return render_template('order-status.html',
                           cache_id=cache_id,
                           order=order_dict,
                           payment=payment,
                           user=user,
                           username=username,
                           cart_item_count=cart_item_count)


@html_views.route('/order-confirmed/', methods=['GET'], strict_slashes=False)
@check_authentication
def order_confirmed():
    """Render the order confirmed page."""
    cache_id = uuid.uuid4()  # Generate a unique cache ID
    user, username, cart_item_count, _ = get_user_and_cart_info()

    # Get the order ID from the request arguments
    order_id = request.args.get('order_id')

    # Retrieve the order by ID
    order = storage.get(Order, order_id)  # Make sure to use your storage method correctly
    
    if not order or order.user_id != user.id:
        return make_response(render_template('404.html'), 404)  # Handle order not found
    
    return render_template('order-confirmed.html',
                           cache_id=cache_id,
                           order_id=order_id,
                           user=user,
                           username=username,
                           cart_item_count=cart_item_count)


