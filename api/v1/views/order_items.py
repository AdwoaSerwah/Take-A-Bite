#!/usr/bin/python3
"""Objects that handle all default RestFul API actions for Order Items"""
from models.order_items import OrderItem
from models import storage
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from flasgger import swag_from

@app_views.route('/order_items', methods=['GET'], strict_slashes=False)
@swag_from('documentation/order_items/all_order_items.yml')
def get_order_items():
    """
    Retrieves the list of all order item objects
    """
    all_order_items = storage.all(OrderItem).values()
    list_order_items = [order_item.to_dict() for order_item in all_order_items]
    return jsonify(list_order_items)

@app_views.route('/order_items/<order_item_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/order_items/get_order_item.yml')
def get_order_item(order_item_id):
    """Retrieves an order item"""
    order_item = storage.get(OrderItem, order_item_id)
    if not order_item:
        abort(404)
    return jsonify(order_item.to_dict())

@app_views.route('/order_items', methods=['POST'], strict_slashes=False)
@swag_from('documentation/order_items/post_order_item.yml')
def post_order_item():
    """
    Creates an order item
    """
    # Ensure request data is JSON
    if not request.get_json():
        return make_response(jsonify({'message': 'No input data provided!'}), 400)

    data = request.get_json()

    # Define the required fields
    required_fields = ['order_id', 'menu_item_id', 'quantity']

    # Check for missing required fields
    for field in required_fields:
        if field not in data:
            return make_response(jsonify({'message': f'Missing {field}'}), 400)

    # Create new order item instance
    instance = OrderItem(**data)
    
    try:
        instance.save()
    except Exception as e:
        return make_response(jsonify({'message': 'An error occurred while saving the order item'}), 500)

    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/order_items/<order_item_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/order_items/put_order_item.yml')
def put_order_item(order_item_id):
    """
    Updates an order item
    """
    # Ensure request data is JSON
    if not request.get_json():
        return make_response(jsonify({'message': 'No fields were modified!'}), 400)

    data = request.get_json()

    # Fetch order item instance
    order_item = storage.get(OrderItem, order_item_id)
    if not order_item:
        return make_response(jsonify({'message': 'Order item not found!'}), 404)

    # Update order item instance
    for field, value in data.items():
        setattr(order_item, field, value)

    # Save updated order item instance
    try:
        order_item.save()
    except Exception as e:
        return make_response(jsonify({'message': 'An error occurred while saving the order item'}), 500)

    return make_response(jsonify(order_item.to_dict()), 200)

@app_views.route('/order_items/<order_item_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/order_items/delete_order_item.yml')
def delete_order_item(order_item_id):
    """
    Deletes an order item object
    """
    order_item = storage.get(OrderItem, order_item_id)

    if not order_item:
        return make_response(jsonify({'message': 'Order item not found!'}), 404)

    storage.delete(order_item)
    storage.save()
    return make_response(jsonify({}), 200)
