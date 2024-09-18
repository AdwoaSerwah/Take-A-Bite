#!/usr/bin/python3
""" Email helper functions """
from flask_mail import Message
from flask import url_for
from api.v1.mail_setup import mail

def send_password_reset_email(user_email, reset_token):
    """Sends a password reset email to the user."""
    msg = Message('Password Reset Request',
                  recipients=[user_email])
    msg.body = f"To reset your password, visit the following link: {url_for('html_views.reset_password', token=reset_token, _external=True)}"
    try:
        mail.send(msg)
        result = "Password reset email sent."
    except Exception as e:
        result = f"Error sending email: {e}"
    return result
