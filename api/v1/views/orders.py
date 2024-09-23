#!/usr/bin/python3
"""Objects that handle all default RestFul API actions for Orders"""
from models.users import User
from models import storage
from flasgger.utils import swag_from
from api.v1.views import app_views
import json
from models.orders import Order, OrderStatus
from models.order_items import OrderItem
from models.menu_items import MenuItem
from models.payments import Payment, PaymentStatus
from flask import abort, jsonify, make_response, request, session, redirect, url_for


@app_views.route('/orders', methods=['GET'], strict_slashes=False)
@swag_from('documentation/orders/get_orders.yml')
def get_orders():
    """
    Retrieves the list of all order objects
    """
    all_orders = storage.all(Order).values()
    list_orders = [order.to_dict() for order in all_orders]
    return jsonify(list_orders)

@app_views.route('/orders/<order_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/orders/get_order.yml')
def get_order(order_id):
    """Retrieves an order"""
    order = storage.get(Order, order_id)
    if not order:
        abort(404)
    return jsonify(order.to_dict())

@app_views.route('/orders', methods=['POST'], strict_slashes=False)
@swag_from('documentation/orders/post_order.yml')
def post_order():
    """
    Creates an order
    """
    if not request.get_json():
        return make_response(jsonify({'message': 'No input data provided!'}), 400)
    
    data = request.get_json()

    # Required fields
    required_fields = ['user_id', 'total_amount']

    # Validate required fields
    for field in required_fields:
        if field not in data:
            return make_response(jsonify({'message': f'Missing {field}'}), 400)
    
    # Create a new order instance
    instance = Order(**data)
    
    try:
        instance.save()
    except Exception as e:
        return make_response(jsonify({'message': 'An error occurred while saving the order'}), 500)
    
    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/orders/<order_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/orders/put_order.yml')
def put_order(order_id):
    """
    Updates an order
    """
    if not request.get_json():
        return make_response(jsonify({'message': 'No fields were modified!'}), 400)
    
    data = request.get_json()

    order = storage.get(Order, order_id)
    if not order:
        abort(404)

    # Update order fields
    for field, value in data.items():
        setattr(order, field, value)
    
    try:
        order.save()
    except Exception as e:
        return make_response(jsonify({'message': 'An error occurred while saving the order'}), 500)
    
    return make_response(jsonify(order.to_dict()), 200)

@app_views.route('/orders/<order_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/orders/delete_order.yml')
def delete_order(order_id):
    """
    Deletes an order object
    """
    order = storage.get(Order, order_id)

    if not order:
        return make_response(jsonify({'message': 'Order not found!'}), 404)

    storage.delete(order)
    storage.save()
    return make_response(jsonify({}), 200)


#if 'user_id' not in session:
        #return redirect(url_for('html_views.login'))


@app_views.route('orders/cart', methods=['POST'], strict_slashes=False)
def add_to_cart():
    """
    Adds to cart
    """
    user_id = session.get('user_id')
    print("User_id: ", user_id)

    if user_id is None:
        return make_response(jsonify({'error': 'User not logged in'}), 403)

    print("REQUEST CONTENT TYPE: ", request.content_type)

    # Ensure request data is JSON
    if not request.get_json():
        return make_response(jsonify({'error': 'Invalid content type, expected JSON'}), 400)

    data = request.get_json()
    menu_item_id = data.get('menu_item_id')
    quantity = int(data.get('quantity', 1))

    if not menu_item_id or quantity <= 0:
        return make_response(jsonify({'error': 'Invalid input'}), 400)

    existing_order = storage.get_pending_order_by_user(user_id)

    if not existing_order:
        existing_order = Order(user_id=user_id, total_amount=0, status='Pending')
        storage.new(existing_order)
        storage.save()

    existing_order_item = None
    for item in storage.all(OrderItem).values():
        if item.order_id == existing_order.id and item.menu_item_id == menu_item_id:
            existing_order_item = item
            break

    if existing_order_item:
        existing_order_item.quantity += quantity
        menu_item = storage.get(MenuItem, menu_item_id)
        if menu_item:
            existing_order_item.price = existing_order_item.quantity * menu_item.price
        storage.save()
    else:
        menu_item = storage.get(MenuItem, menu_item_id)
        if not menu_item:
            return make_response(jsonify({'error': 'Menu item not found'}), 404)

        new_order_item = OrderItem(
            order_id=existing_order.id,
            menu_item_id=menu_item_id,
            quantity=quantity,
            price=menu_item.price * quantity
        )
        storage.new(new_order_item)
        storage.save()

    total_amount = storage.calculate_order_total(existing_order.id)
    existing_order.total_amount = total_amount
    storage.save()

    return make_response(jsonify({'message': 'Item added to cart successfully'}), 200)


@app_views.route('/update_cart_item/<menu_item_id>', methods=['POST'])
def update_cart_item(menu_item_id):
    """
    Update the quantity of a cart item using the menu_item_id
    """
    user_id = session.get('user_id')
    
    # Ensure the user is logged in
    if user_id is None:
        return make_response(jsonify({'error': 'User not logged in'}), 403)
    
    # Ensure request data is JSON
    if not request.get_json():
        return make_response(jsonify({'error': 'Invalid content type, expected JSON'}), 400)
    
    data = request.get_json()
    new_quantity = int(data.get('quantity', 0))  # Convert to integer
    
    if new_quantity <= 0 or new_quantity > 10:
        return make_response(jsonify({'error': 'Invalid quantity, must be between 1 and 10'}), 400)
    
    # Get the user's pending order
    existing_order = storage.get_pending_order_by_user(user_id)
    
    if not existing_order:
        return make_response(jsonify({'error': 'No pending order found'}), 404)
    
    # Find the matching order item by menu_item_id
    order_item = None
    for item in existing_order.order_items:
        if item.menu_item_id == menu_item_id:
            order_item = item
            break
    
    if order_item is None:
        return make_response(jsonify({'error': 'Item not found in cart'}), 404)
    
    # Update the order item quantity
    order_item.quantity = new_quantity
    order_item.price = order_item.quantity * order_item.menu_item.price
    storage.save()

    # Recalculate cart subtotal and item count
    cart_subtotal = sum(item.quantity * item.menu_item.price for item in existing_order.order_items)
    cart_item_count = sum(item.quantity for item in existing_order.order_items)

    # Format cart_subtotal to two decimal places
    formatted_cart_subtotal = round(cart_subtotal, 2)


    # Update the order total
    existing_order.total_amount = formatted_cart_subtotal
    storage.save()

    # Format total_item_price to two decimal places
    formatted_total_item_price = round(order_item.price, 2)

    return jsonify({
        'success': True,
        'total_item_price': formatted_total_item_price,
        'cart_subtotal': formatted_cart_subtotal,
        'cart_item_count': cart_item_count
    })


@app_views.route('/remove_cart_item/<menu_item_id>', methods=['POST'])
def remove_cart_item(menu_item_id):
    user_id = session.get('user_id')

    if user_id is None:
        return make_response(jsonify({'error': 'User not logged in'}), 403)

    existing_order = storage.get_pending_order_by_user(user_id)

    if not existing_order:
        return make_response(jsonify({'error': 'No pending order found'}), 404)

    order_item = next((item for item in existing_order.order_items if item.menu_item_id == menu_item_id), None)

    if not order_item:
        return make_response(jsonify({'error': 'Item not found in cart'}), 404)

    existing_order.order_items.remove(order_item)
    storage.save()

    # If no items are left in the cart, delete the order and its payment
    if not existing_order.order_items:
        existing_payment = storage.get_payment_by_order(existing_order.id)
        if existing_payment:
            storage.delete(existing_payment)  # Delete associated payment
        storage.delete(existing_order)  # Delete the order
        storage.save()
        return jsonify({
            'success': True,
            'cart_item_count': 0,
            'cart_subtotal': 0
        })

    # Recalculate cart subtotal and item count
    cart_subtotal = sum(item.quantity * item.menu_item.price for item in existing_order.order_items)
    cart_item_count = sum(item.quantity for item in existing_order.order_items)

    # Update the order total
    existing_order.total_amount = cart_subtotal
    storage.save()

    return jsonify({
        'success': True,
        'cart_item_count': cart_item_count,
        'cart_subtotal': cart_subtotal
    })


@app_views.route('/update-location-payment', methods=['POST'])
def update_location_payment():
    """
    Process the checkout with the selected payment method and order details.
    """
    user_id = session.get('user_id')
    
    # Ensure the user is logged in
    if user_id is None:
        return make_response(jsonify({'success': False, 'error': 'User not logged in'}), 403)

    # Ensure request data is JSON
    if not request.get_json():
        return make_response(jsonify({'success': False, 'error': 'Invalid content type, expected JSON'}), 400)

    data = request.get_json()

    # Validate the data
    total = data.get('total')
    payment_method = data.get('payment_method')
    location_id = data.get('location_id')  # Get location ID from request

    # Retrieve the user's pending order
    existing_order = storage.get_pending_order_by_user(user_id)
    
    if not existing_order:
        return make_response(jsonify({'success': False, 'error': 'No pending order found'}), 404)

    # Update the order's location ID
    existing_order.location_id = location_id  # Update location ID

    # Check for existing payment
    existing_payment = storage.get_payment_by_order(existing_order.id)

    if existing_payment:
        # Update existing payment
        existing_payment.amount = total
        existing_payment.method = payment_method
        existing_payment.status = PaymentStatus.PENDING
        storage.save()
    else:
        # Create a new payment record if no existing payment found
        payment = Payment(
            amount=total,
            method=payment_method,
            status=PaymentStatus.PENDING,
            order_id=existing_order.id  # Link to the existing order
        )
        # Save the payment to the database
        storage.new(payment)
        storage.save()

    # If payment method is 'Cash', mark the order as completed
    if payment_method.lower() == 'cash':
        existing_order.status = OrderStatus.COMPLETED
        storage.save()


    # Return success response with order ID
    return jsonify({'success': True, 'order_id': existing_order.id})
