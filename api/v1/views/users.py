#!/usr/bin/python3
"""Objects that handle all default RestFul API actions for Users"""
from models.users import User
from models import storage
from flask import abort, jsonify, make_response, request, session, redirect, url_for # , flash
from flasgger.utils import swag_from
from datetime import datetime, timezone
from api.v1.views import app_views  #, send_password_reset_email
from utils.email_utils import send_password_reset_email 
import re
import json
from models.orders import Order
from models.order_items import OrderItem
from models.menu_items import MenuItem
# from sqlalchemy.exc import IntegrityError


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_users.yml')
def get_users():
    """
    Retrieves the list of all user objects
    """
    if 'user_id' not in session:
        return redirect(url_for('login_user'))  # Redirect to login if not authenticated

    all_users = storage.all(User).values()
    list_users = [user.to_dict() for user in all_users]
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_user(user_id):
    """Retrieves a user"""
    if 'user_id' not in session:
        return redirect(url_for('login_user'))  # Redirect to login if not authenticated

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a user object
    """
    user = storage.get(User, user_id)

    if not user:
        return make_response(jsonify({'message': 'User not found!'}), 401)

    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/post_user.yml', methods=['POST'])
def post_user():
    """
    Creates a user
    """
    # Ensure request data is JSON
    if not request.get_json():
        return make_response(jsonify({'message': 'No input data provided!'}), 400)

    data = request.get_json()

    # Define the required fields
    required_fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']

    # Check for missing required fields
    for field in required_fields:
        if field not in data:
            return make_response(jsonify({'message': f'Missing {field}'}), 400)

    # Check for existing username
    username = data.get('username')
    if storage.get_by_username(User, username):
        print("User already exists!")
        return make_response(jsonify({'message': 'Username already exists!'}), 400)

    # Check for existing email
    email = data.get('email')
    if storage.get_by_email(User, email):
        return make_response(jsonify({'message': 'Email already registered!'}), 400)

    # Check for existing phone number
    phone = data.get('phone_number')
    if storage.get_by_phone(User, phone):
        return make_response(jsonify({'message': 'Phone number already registered!'}), 400)

    # Create new user instance
    instance = User(**data)
    
    try:
        instance.save()
    except Exception as e:
        return make_response(jsonify({'message': 'An error occurred while saving the user'}), 500)

    # Set session after successful registration
    session['user_id'] = instance.id

    return make_response(jsonify(instance.to_dict()), 201)



@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/user/put_user.yml', methods=['PUT'])
def put_user(user_id):
    """
    Updates a user
    """
    # Ensure request data is JSON
    if not request.get_json():
        return make_response(jsonify({'message': 'No fields were modified!'}), 400)

    data = request.get_json()

    # Fetch user instance
    user = storage.get(User, user_id)
    if not user:
        return make_response(jsonify({'message': 'User not found!'}), 404)
    
    # Dictionary for field-specific unique checks
    unique_checks = {
        'username': storage.get_by_username,
        'email': storage.get_by_email,
        'phone_number': storage.get_by_phone
    }

    # Iterate over the fields in the data
    for field, value in data.items():
        if field == 'username' or field == 'email' or field == 'phone_number':
            # Perform unique validation only for specific fields
            if unique_checks.get(field)(User, value) and getattr(user, field) != value:
                return make_response(jsonify({'message': f'{field.capitalize()} already exists!'}), 400)

        # Update user instance
        setattr(user, field, value)

    # Save updated user instance
    try:
        user.save()
    except Exception as e:
        return make_response(jsonify({'message': 'An error occurred while saving the user'}), 500)

    return make_response(jsonify(user.to_dict()), 200)


@app_views.route('/login', methods=['POST'], strict_slashes=False)
def login_user():
    """
    Logs in a user by checking credentials
    """
    if not request.get_json():
        return make_response(jsonify({'message': 'No input data provided!'}), 400)
        # abort(400, description="Not a JSON")

    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return make_response(jsonify({'message': 'Missing username or password'}), 400)


    # Use the all() method to get all User objects
    all_users = storage.all(User)  # Get all users from storage

    # Search for the user by username
    user = None
    for u in all_users.values():
        if u.username == data['username']:
            user = u
            break

    # If user not found or password does not match, return 401
    if not user:
        return make_response(jsonify({'message': 'User not found!'}), 401)

    if not user.check_password(data['password']):
        return make_response(jsonify({'message': 'Password is incorrect!'}), 401)

    # Store user ID in the session for authentication
    session['user_id'] = user.id

        # Sync local cart with server
    cart_items = request.cookies.get('cart')  # Retrieve cart from cookies or local storage
    if cart_items:
        # Add logic to transfer cart items to the user’s account
        user = storage.get(User, user_id)
        user.cart = json.loads(cart_items)
        storage.save()
        response.delete_cookie('cart')  # Remove the temporary cart cookie

    return make_response(jsonify({'message': 'Logged in successfully'}), 200)


@app_views.route('/forgot-password', methods=['POST'], strict_slashes=False)
def forgot_password():
    """
    Handles the forgot password request.
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    if not data or 'email' not in data:
        return make_response(jsonify({'message': 'Missing email'}), 400)
    email = data['email']

    # Look up the user by email
    user = storage.get_by_email(User, email=email)
    if user is None:
        return make_response(jsonify({'message': 'User not found!'}), 404)
        # abort(404, description="User not found")

    # Generate a reset token and save it
    user.generate_reset_token()
    print(user.reset_token)
    print(user.email)

    # Send the password reset email
    result = send_password_reset_email(user.email, user.reset_token)
    # Flash a message
    # flash('An email has been sent to your email address.')

    return make_response(jsonify({'message': result}), 200)

@app_views.route('/reset-password/<token>', methods=['POST'], strict_slashes=False)
def reset_password(token):
    """
    Handles the actual password reset using a token.
    """
    user = storage.get_by_token(token)

    # print(f"{datetime.now(timezone.utc)}: {type(datetime.now(timezone.utc))}")
    # print(f"{user.token_expiry}: {type(user.token_expiry)}")

    # Check if user and token are valid
    if not user:
        return make_response(jsonify({'message': 'Invalid or expired token'}), 400)

    if user.token_expiry.tzinfo is None:
        user.token_expiry = user.token_expiry.replace(tzinfo=timezone.utc)

    if datetime.now(timezone.utc) > user.token_expiry:
        return make_response(jsonify({'message': 'Token expired'}), 400)

    # Proceed to reset the password
    data = request.get_json()
    print(f"data: {data}")
    if 'new_password' not in data:
        return make_response(jsonify({'message': 'New password required'}), 400)

    user.set_password(data['new_password'])  # Assume a method to update the password
    print(f"Password: {user.password}")
    user.reset_token = None
    user.token_expiry = None
    user.save()

    return make_response(jsonify({'message': 'Password reset successful'}), 200)



@app_views.route('/logout', methods=['POST'], strict_slashes=False)
def logout_user():
    """
    Logs out a user by clearing the session
    """
    session.pop('user_id', None)
    return redirect(url_for('html_views.home'))
