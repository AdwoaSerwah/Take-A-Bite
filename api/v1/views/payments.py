#!/usr/bin/python3
"""Objects that handle all default RestFul API actions for Payments"""
from models.payments import Payment, PaymentStatus
from models import storage
from flask import abort, jsonify, make_response, request, session
from api.v1.views import app_views
from flasgger.utils import swag_from
from api.v1.views import app_views


@app_views.route('/payments', methods=['GET'], strict_slashes=False)
@swag_from('documentation/payments/all_payments.yml')
def get_payments():
    """
    Retrieves the list of all payment objects
    """
    all_payments = storage.all(Payment).values()
    list_payments = [payment.to_dict() for payment in all_payments]
    return jsonify(list_payments)

@app_views.route('/payments/<payment_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/payments/get_payment.yml')
def get_payment(payment_id):
    """Retrieves a payment"""
    payment = storage.get(Payment, payment_id)
    if not payment:
        abort(404)
    return jsonify(payment.to_dict())

@app_views.route('/payments', methods=['POST'], strict_slashes=False)
@swag_from('documentation/payments/post_payment.yml')
def post_payment():
    """
    Creates a payment
    """
    # Ensure request data is JSON
    if not request.get_json():
        return make_response(jsonify({'message': 'No input data provided!'}), 400)

    data = request.get_json()

    # Define the required fields
    required_fields = ['order_id', 'amount', 'payment_method', 'status']

    # Check for missing required fields
    for field in required_fields:
        if field not in data:
            return make_response(jsonify({'message': f'Missing {field}'}), 400)

    # Create new payment instance
    instance = Payment(**data)
    
    try:
        instance.save()
    except Exception as e:
        return make_response(jsonify({'message': 'An error occurred while saving the payment'}), 500)

    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/payments/<payment_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/payments/put_payment.yml')
def put_payment(payment_id):
    """
    Updates a payment
    """
    # Ensure request data is JSON
    if not request.get_json():
        return make_response(jsonify({'message': 'No fields were modified!'}), 400)

    data = request.get_json()

    # Fetch payment instance
    payment = storage.get(Payment, payment_id)
    if not payment:
        return make_response(jsonify({'message': 'Payment not found!'}), 404)

    # Update payment instance
    for field, value in data.items():
        setattr(payment, field, value)

    # Save updated payment instance
    try:
        payment.save()
    except Exception as e:
        return make_response(jsonify({'message': 'An error occurred while saving the payment'}), 500)

    return make_response(jsonify(payment.to_dict()), 200)

@app_views.route('/payments/<payment_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/payments/delete_payment.yml')
def delete_payment(payment_id):
    """
    Deletes a payment object
    """
    payment = storage.get(Payment, payment_id)

    if not payment:
        return make_response(jsonify({'message': 'Payment not found!'}), 404)

    storage.delete(payment)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/update-payment', methods=['POST'])
def update_payment():
    """
    Update the payment and order status after a successful transaction.
    """
    user_id = session.get('user_id')
    
    # Ensure the user is logged in
    print("I am here!")
    if user_id is None:
        return make_response(jsonify({'success': False, 'error': 'User not logged in'}), 403)

    # Ensure request data is JSON
    if not request.get_json():
        return make_response(jsonify({'success': False, 'error': 'Invalid content type, expected JSON'}), 400)

    data = request.get_json()

    # Validate the data
    order_id = data.get('order_id')
    payment_status = data.get('payment_status')
    transaction_ref = data.get('transaction_ref')  # Get transaction reference from Paystack

    # Retrieve the user's pending order using the order ID
    existing_order = storage.get_order_by_id(order_id)
    
    if not existing_order:
        return make_response(jsonify({'success': False, 'error': 'Order not found'}), 404)
    
    if existing_order:
        if existing_order.status == 'COMPLETED':
            return make_response(jsonify({'success': False, 'error': 'Payment has already been completed.'}), 400)


    # Check for existing payment
    existing_payment = storage.get_payment_by_order(existing_order.id)

    if existing_payment:
        # Update existing payment with status and transaction reference
        existing_payment.status = PaymentStatus.COMPLETED if payment_status == 'COMPLETED' else PaymentStatus.FAILED
        existing_payment.transaction_ref = transaction_ref  # Store transaction reference
        storage.save()
    else:
        return make_response(jsonify({'success': False, 'error': 'No payment found for the order'}), 404)

    # If payment was successful, update the order status
    if payment_status == 'COMPLETED':
        existing_order.status = 'COMPLETED'  # Or whatever status you use for completed orders
        storage.save()

    # Return success response
    return jsonify({'success': True, 'message': 'Payment and order status updated successfully'})

