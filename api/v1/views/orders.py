#!/usr/bin/python3
"""Objects that handle all default RestFul API actions for Orders"""
from models.users import User
from models import storage
from flasgger.utils import swag_from
from api.v1.views import app_views
import json
from models.orders import Order
from models.order_items import OrderItem
from models.menu_items import MenuItem
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


