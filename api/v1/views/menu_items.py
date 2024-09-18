#!/usr/bin/python3
"""Objects that handle all default RestFul API actions for MenuItems"""
from models.menu_items import MenuItem
from models import storage
from flask import abort, jsonify, make_response, request, session, redirect, url_for
from flasgger.utils import swag_from
from api.v1.views import app_views
from models.order_items import OrderItem
from models.menu_items import MenuItem
from models.orders import Order


@app_views.route('/menu_items', methods=['GET'], strict_slashes=False)
@swag_from('documentation/menu_item/all_menu_items.yml')
def get_menu_items():
    """
    Retrieves the list of all menu item objects
    """
    all_items = storage.all(MenuItem).values()
    list_items = [item.to_dict() for item in all_items]
    return jsonify(list_items)


@app_views.route('/menu_items/<menu_item_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/menu_item/get_menu_item.yml', methods=['GET'])
def get_menu_item(menu_item_id):
    """Retrieves a menu item"""
    item = storage.get(MenuItem, menu_item_id)
    if not item:
        abort(404)
    return jsonify(item.to_dict())


@app_views.route('/menu_items/<menu_item_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/menu_item/delete_menu_item.yml', methods=['DELETE'])
def delete_menu_item(menu_item_id):
    """
    Deletes a menu item object
    """
    item = storage.get(MenuItem, menu_item_id)
    if not item:
        return make_response(jsonify({'message': 'Menu item not found!'}), 404)

    storage.delete(item)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/menu_items', methods=['POST'], strict_slashes=False)
@swag_from('documentation/menu_item/post_menu_item.yml', methods=['POST'])
def post_menu_item():
    """
    Creates a menu item
    """
    # Ensure request data is JSON
    if not request.get_json():
        return make_response(jsonify({'message': 'No input data provided!'}), 400)

    data = request.get_json()

    # Define the required fields
    required_fields = ['name', 'price', 'description', 'category_id']

    # Check for missing required fields
    for field in required_fields:
        if field not in data:
            return make_response(jsonify({'message': f'Missing {field}'}), 400)

    # Create new menu item instance
    instance = MenuItem(**data)
    
    try:
        instance.save()
    except Exception as e:
        return make_response(jsonify({'message': 'An error occurred while saving the menu item'}), 500)

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/menu_items/<menu_item_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/menu_item/put_menu_item.yml', methods=['PUT'])
def put_menu_item(menu_item_id):
    """
    Updates a menu item
    """
    # Ensure request data is JSON
    if not request.get_json():
        return make_response(jsonify({'message': 'No fields were modified!'}), 400)

    data = request.get_json()

    # Fetch menu item instance
    item = storage.get(MenuItem, menu_item_id)
    if not item:
        return make_response(jsonify({'message': 'Menu item not found!'}), 404)
    
    # Update menu item instance
    for field, value in data.items():
        setattr(item, field, value)

    # Save updated menu item instance
    try:
        item.save()
    except Exception as e:
        return make_response(jsonify({'message': 'An error occurred while saving the menu item'}), 500)

    return make_response(jsonify(item.to_dict()), 200)


@app_views.route('/menu_items/category/<category_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/menu_item/menu_item_by_category.yml', methods=['GET'])
def get_menu_items_by_category(category_id):
    """
    Retrieves menu items filtered by category ID
    """
    all_menu_items = storage.all(MenuItem).values()
    filtered_menu_items = [item.to_dict() for item in all_menu_items if item.category_id == category_id]

    if not filtered_menu_items:
        return make_response(jsonify({'message': 'No menu items found for this category!'}), 404)

    return jsonify(filtered_menu_items)


@app_views.route('/menu_items/name/<name>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/menu_item/menu_item_by_name.yml', methods=['GET'])
def get_menu_items_by_name(name):
    """
    Retrieves menu items filtered by name
    """
    all_menu_items = storage.all(MenuItem).values()
    filtered_menu_items = [item.to_dict() for item in all_menu_items if name.lower() in item.name.lower()]

    if not filtered_menu_items:
        return make_response(jsonify({'message': 'No menu items found with this name!'}), 404)

    return jsonify(filtered_menu_items)
