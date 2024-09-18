#!/usr/bin/python3
"""Objects that handle all default RestFul API actions for Locations"""
from models.locations import Location
from models import storage
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from flasgger import swag_from

@app_views.route('/locations', methods=['GET'], strict_slashes=False)
@swag_from('documentation/location/all_locations.yml')
def get_locations():
    """
    Retrieves the list of all location objects
    """
    all_locations = storage.all(Location).values()
    list_locations = [location.to_dict() for location in all_locations]
    return jsonify(list_locations)

@app_views.route('/locations/<location_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/location/get_location.yml')
def get_location(location_id):
    """Retrieves a location"""
    location = storage.get(Location, location_id)
    if not location:
        abort(404)
    return jsonify(location.to_dict())

@app_views.route('/locations', methods=['POST'], strict_slashes=False)
@swag_from('documentation/location/post_location.yml')
def post_location():
    """
    Creates a location
    """
    # Ensure request data is JSON
    if not request.get_json():
        return make_response(jsonify({'message': 'No input data provided!'}), 400)

    data = request.get_json()

    # Define the required fields
    required_fields = ['name', 'address']

    # Check for missing required fields
    for field in required_fields:
        if field not in data:
            return make_response(jsonify({'message': f'Missing {field}'}), 400)

    # Create new location instance
    instance = Location(**data)
    
    try:
        instance.save()
    except Exception as e:
        return make_response(jsonify({'message': 'An error occurred while saving the location'}), 500)

    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/locations/<location_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/location/put_location.yml')
def put_location(location_id):
    """
    Updates a location
    """
    # Ensure request data is JSON
    if not request.get_json():
        return make_response(jsonify({'message': 'No fields were modified!'}), 400)

    data = request.get_json()

    # Fetch location instance
    location = storage.get(Location, location_id)
    if not location:
        return make_response(jsonify({'message': 'Location not found!'}), 404)

    # Update location instance
    for field, value in data.items():
        setattr(location, field, value)

    # Save updated location instance
    try:
        location.save()
    except Exception as e:
        return make_response(jsonify({'message': 'An error occurred while saving the location'}), 500)

    return make_response(jsonify(location.to_dict()), 200)

@app_views.route('/locations/<location_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/location/delete_location.yml')
def delete_location(location_id):
    """
    Deletes a location object
    """
    location = storage.get(Location, location_id)

    if not location:
        return make_response(jsonify({'message': 'Location not found!'}), 404)

    storage.delete(location)
    storage.save()
    return make_response(jsonify({}), 200)
