#!/usr/bin/python3
"""Handles routes for contract"""
from api.v1.views import api_views
from flask import abort, session, request, make_response, jsonify
import jwt
from models.contract import Contract
from models.user import Review, User
from models import storage

from api.v1.views.token import requires_token

def calc_tot_rate(user_id):
    """Calculates and stores the rating avg of user"""
    user = storage.get(User, user_id)
    _session = storage.session()
    reviews = _session.query(Review).filter(Review.for_user_id==user_id).all()
    total = 0
    count = 1
    for review in reviews:
        total += review.rating
        count += 1
    rate_tot = total / count
    user.rating = rate_tot
    _session.add(user)
    storage.save
@api_views.route('/contracts/<contract_id>/rate',
           methods=['POST'], strict_slashes=False)
def rate_contract(contract_id):
    """Rating and review of contract by Buyer"""
    if not request.get_json():
        abort(400, 'Not a JSON')

    _session = storage.session()

    """try:
        user_id = session['user_id']
    except:
        token = request.headers['x-access-tokens']
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user_id = data['user_id']
    else:
        return make_response(jsonify({'message': 'Login required'}), 400)"""

    contract = _session.query(Contract).\
            filter(Contract.id==contract_id).first()
    if not contract:
        abort(404, 'Contract Not Found')
    if request.get_json()['buyer_id'] == contract.buyer_id:
        req = request.get_json()
        if 'rate' not in req.keys() and 'review' not in req.keys():
            return make_response(jsonify({'error': 'Invalid data for rating',
                                          'valid': 'rate, review'}), 400)
        rate = int(req.get('rate'))
        review = req.get('review')
        seller_id = contract.seller_id

        new_review = Review(by_user_id=request.get_json()['buyer_id'],
                            for_user_id=seller_id,
                            review_body=review, rating=rate)
        storage.new(new_review)
        storage.save()
        calc_tot_rate(seller_id)
        return make_response(jsonify({'message': 'Rated and reviews successfully'}), 200)
    return make_response(jsonify({'error': 'Error updating data'}), 501)

@api_views.route('/contracts/<contract_id>/initiate',
                 methods=['POST'], strict_slashes=False)
def initiate_con(contract_id):
    """Initiate contract by Seller"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'status' not in request.get_json().keys():
        abort(400, 'Invalid data')
    _session = storage.session()
    try:
        user_id = session['user_id']
    except:
        token = request.headers['x-access-tokens']
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user_id = data['user_id']
    else:
        return make_response(jsonify({'message': 'Login required'}), 400)
    contract = _session.query(Contract).filter(Contract.id==contract_id).first()
    if not contract:
        abort(404, 'Contract Not Found')
    req = request.get_json()

    if user_id == contract.seller_id:
        for k, v in req.items():
            setattr(contract, k, v)
        storage.save()
        return make_response(jsonify({'message': 'Contract updated sucessfully'}),
                             200)
    else:
        abort(400, 'Login rquired')

@api_views.route('/contracts/<contract_id>', methods=['GET'],
                 strict_slashes=False)
def contract_view(contract_id):
    """View Contract by Seller or Buyer"""
    try:
        user_id = session['user_id']
    except:
        token = request.headers['x-access-tokens']
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user_id = data['user_id']
    else:
        return make_response(jsonify({'message': 'Login required'}), 400)

    _session = storage.session()
    contract = _session.query(Contract).\
            filter(Contract.id==contract_id).first()
    if not contract:
        abort(404, 'Contract Not Found')
    if contract.seller_id == user_id or contract.buyer_id == user_id:
        return make_response(jsonify(contract.to_dict()), 200)
    else:
        abort(400)
@api_views.route('/contracts/create', methods=['POST'], strict_slashes=False)
def contract_create():
    """User create Contract as Buyer"""
    """try:
        user_id = session['user_id']
    except:
        token = request.headers['x-access-tokens']
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user_id = data['user_id']
    else:
        make_response(jsonify({'message': 'Login required'}), 400)"""
    if not request.get_json():
        abort(400, 'Not a JSON')

    r_keys = ['c_type', 's_user',
              'b_user', 'name',
              'desc', 'amount']
    req = request.get_json()
    for key in r_keys:
        if key not in req:
            abort(400, '{} required'.format(key))
    """if req['b_user'] != session['user_name']:
        return jsonify({'message': 'unauthorized access'})"""
    _session = storage.session()
    c_type = req['c_type']
    seller= req['s_user']
    buyer = req['b_user']
    s_user = _session.query(User).filter(User.user_name==seller).first()
    b_user = _session.query(User).filter(User.user_name==buyer).first()
    seller_id = s_user.id
    buyer_id = b_user.id
    name = req['name']
    descr = req['desc']
    status = 'created'
    amount = float(req['amount'])

    new_contract = Contract(c_type=c_type, seller_id=seller_id,
                            buyer_id=buyer_id, name=name, description=descr,
                            status=status, amount=amount)
    storage.new(new_contract)
    storage.save()
    return make_response(jsonify({'messaege': 'Contract Created Successfully'}),
                         200)

@api_views.route('/contracts/<contract_id>/dispute',
                 methods=['POST'], strict_slashes=False)
def dispute_contract(contract_id):
    """Buyer(User) sets contract status to disputed and automatically
    send 0 rating review with issue as review"""
    if not request.get_json():
        abort(400, 'Not a JSON')

    """try:                                                                                        user_id = session['user_id']                                                        except:
        token = request.headers['x-access-tokens']                                              data = jwt.decode(token, app.config['SECRET_KEY'])                                      user_id = data['user_id']                                                           else:
        make_response(jsonify({'message': 'Login required'}), 400)"""

    contract = _session.query(Contract).\
            filter(Contract.id==contract_id).first()
    if not contract:
        abort(404, 'Contract Not Found')

    if user_id == contract.buyer_id:
        req = request.get_json()
        if 'issue' not in req.keys():
            abort(400, 'Invalid data')
        review = Review(by_user_id=user_id, for_user_id=contract.seller_id,
                        review_body=req['issue'], rating=0)
        contract.disputed = 1
        contract.status = 'disputed'
        storage.new(review)
        storage.save()
        return make_reponse(jsonify({'message': 'Dispute review sent successfully'}), 200)
    abort(500)
