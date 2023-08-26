#!/usr/bin/python
from api.v1.views import api_views
from api.v1.views.token import requires_token
from datetime import datetime
from flask import abort, jsonify, make_response, request, session
import jwt
from models import storage
from models.user import User, Review
import re
from werkzeug.security import generate_password_hash, check_password_hash

@api_views.route('/login', methods=['POST'], strict_slashes=False)
def login():
    if not request.get_json():
        abort(400, 'Not a JSON')
    elif 'email' not in request.get_json().keys()\
            and 'password' not in request.get_json().keys():
        return make_response(jsonify(
            {'message': 'invalid data for authorization'}),
                             400)
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user_id = storage.get_id('User', email)
    user = storage.get(User, user_id)

    if check_password_hash(user.password, password):
        session['user_id'] = user_id
        session['user_name'] = user.user_name
        token = jwt.encode({'user_id': user_id,
                           'exp': datetime.now() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response(jsonify({'message': 'Could not verify'}), 400)

@api_views.route('/register', methods=['POST'], strict_slashes=False)
def register():
    if not request.get_json():
        abort(400, 'Not a JSON')
    valids = ['name', 'email', 'phone', 'user_name', 'password']
    data = request.get_json()
    keys = []
    _session = storage.session()

    for k in data.keys():
        keys.append(k)
    keys.sort()
    valids.sort()
    if  keys != valids:
        return make_response(jsonify({
            'message': 'Incomplete Data, Complete with data {}'.format(valids)}),
                             400)
    name = data.get('name')
    email = data.get('email')
    user_name = data.get('user_name')
    phone = data.get('phone')

    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return make_response(jsonify({'message': 'Invalid email'}), 400)

    if not re.match(r'[A-Za-z0-9]+', user_name):
        note = 'Invalid username, use only [A-Zz-a0-9] range of characters'
        return make_response(jsonify({'message': note}), 400)

    acct_exists = _session.query(User).\
            filter(User.email==email).first()
    if acct:
        return make_response(jsonify({'message': 'user with email already exists'}), 400)
    user_exists = _session.query(User).\
            filter(User.user_name==user_name).first()
    if user_exists:
        return make_response(jsonify({'message': 'username is taken'}), 400)

    password = generate_password_hash(data.get('password'), method='md5')
    new_user = User(name=name, email=email,
                    user_name=user_name, phone=phone,
                    password=password)

    storage.add(new_user)
    storage.save()

    return make_response(jsonify({'message': 'user {} is registered successfully'}),
                         200)

def _profile_view(user_name):
    _session = storage.session()
    user = _session.query(User).filter(User.user_name==user_name).first()
    if not user:
        return {'message': 'User with username {} does not exist'.\
                format(user_name), 'status': 400}
    user_id = user.id
    business = _session.query(Business).filter(Business.user_id==user_id).first()
    reviews = _session.query(Review).\
            filter(Review.for_user_id==user_id).order_by(Reviews.rating)
    revs = []
    if reviews:
        for review in reviews:
            by_user = review.by_user_id
            by_user = _session.query(User).filter(User.id==by_user).first()
            by_username = by_user.user_name
            review = review.to_dict()
            review.update({'Review_By': by_username})
            review.pop('for_user_id')
            revs.append(review)
    full_dict = user.to_dict()
    full_dict.pop('password')
    if business:
        business = business.to_dict()
        business.pop('id')
        business.pop('user_id')
        full_dict.update(business)
    full_dict.update({'reviews': revs})
    full_dict.update({'status': 200})
    return full_dict

@api_views.route('/users/<user_name>', methods=['GET'], strict_slashes=False)
def guess_profile_view(user_name):
    full_dict = _profile_view(user_name)
    status_code = full_dict.get('status', 501)
    return make_response(jsonify(full_dict), status_code)

@api_views.route('/user/<user_name>/profile',
                 methods=['GET', 'PUT'], strict_slashes=False)
@requires_token()
def profile_ract(user_name):
    if request.method == 'GET':
        full_dict = _profile_view(user_name)

    if request.method == 'PUT':
        _session = storage.session()
        user = _session.query(User).filter(User.user_name==user_name).first()
        if request.get_json():
            data = request.get_json()
            ignore = ['password', 'user_name', 'email', 'created_at', 'id']
            for k, v in data.items():
                if k not in ignore:
                    setattr(user, k, v)
            storage.save()
            full_dict = _profile_view(user_name)
            status_code = full_dict.get('status', 501)
            return make_response(jsonify(full_dict), status_code)
        else:
            abort(400, 'Not a JSON')
    abort(501, 'Something went wrong or method not available')
