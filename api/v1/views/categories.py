#!/usr/bin/python3
"""Objects that handle all default RestFul API actions for Categories"""
from models.categories import Category
from models import storage
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from flasgger import swag_from

@app_views.route('/categories', methods=['GET'], strict_slashes=False)
@swag_from('documentation/category/all_categories.yml')
def get_categories():
    """
    Retrieves the list of all category objects
    """
    all_categories = storage.all(Category).values()
    list_categories = [category.to_dict() for category in all_categories]
    return jsonify(list_categories)

@app_views.route('/categories/<category_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/category/get_category.yml')
def get_category(category_id):
    """Retrieves a category"""
    category = storage.get(Category, category_id)
    if not category:
        abort(404)
    return jsonify(category.to_dict())

@app_views.route('/categories', methods=['POST'], strict_slashes=False)
@swag_from('documentation/category/post_category.yml')
def post_category():
    """
    Creates a category
    """
    # Ensure request data is JSON
    if not request.get_json():
        return make_response(jsonify({'message': 'No input data provided!'}), 400)

    data = request.get_json()

    # Define the required fields
    required_fields = ['name']

    # Check for missing required fields
    for field in required_fields:
        if field not in data:
            return make_response(jsonify({'message': f'Missing {field}'}), 400)

    # Create new category instance
    instance = Category(**data)
    
    try:
        instance.save()
    except Exception as e:
        return make_response(jsonify({'message': 'An error occurred while saving the category'}), 500)

    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/categories/<category_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/category/put_category.yml')
def put_category(category_id):
    """
    Updates a category
    """
    # Ensure request data is JSON
    if not request.get_json():
        return make_response(jsonify({'message': 'No fields were modified!'}), 400)

    data = request.get_json()

    # Fetch category instance
    category = storage.get(Category, category_id)
    if not category:
        return make_response(jsonify({'message': 'Category not found!'}), 404)

    # Update category instance
    for field, value in data.items():
        setattr(category, field, value)

    # Save updated category instance
    try:
        category.save()
    except Exception as e:
        return make_response(jsonify({'message': 'An error occurred while saving the category'}), 500)

    return make_response(jsonify(category.to_dict()), 200)

@app_views.route('/categories/<category_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/category/delete_category.yml')
def delete_category(category_id):
    """
    Deletes a category object
    """
    category = storage.get(Category, category_id)

    if not category:
        return make_response(jsonify({'message': 'Category not found!'}), 404)

    storage.delete(category)
    storage.save()
    return make_response(jsonify({}), 200)
