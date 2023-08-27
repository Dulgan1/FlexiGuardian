#!/usr/bin/python3
from functools import wraps
from flask import session, jsonify, request
import jwt
from models import storage
from os import getenv

def requires_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        _session = storage.session()
        if 'user_id' in session and 'user_name' in session:
            user_name = session['user_name']
            return f(user_name, *args, **kwargs)
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        try:
            data = jwt.decode(token, getenv('FG_SECRET_KEY'))
            user = _session.query(User).filter(User.id==data['user_id']).first()
            user_name = user.user_name
        except:
            return jsonify({'message':'token is invalid2222'})
        return f(user_name, *args, **kwargs)
    return decorator
