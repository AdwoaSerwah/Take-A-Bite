"""This module checks for user authentications"""
from flask import session, redirect, url_for
from functools import wraps

def check_authentication(f):
    """Check if a user has logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('html_views.login'))
        return f(*args, **kwargs)
    return decorated_function
