""" Defined for authentication,
    @requires_token decorator"""
from functools import wraps
from flask import session, redirect, url_for, flash
from models import storage

def requires_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'user_id' in session:
            user_id = session['user_id']
            return f(user_id, *args, **kwargs)
        else:
            flash('Login required')
            return redirect(url_for('app_views.login'))
    return decorator
