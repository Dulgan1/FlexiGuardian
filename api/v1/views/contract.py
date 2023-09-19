#!/usr/bin/python3
"""Handles routes for contract"""
from api.v1.views import api_views
from flask import abort, session, request, make_response, jsonify
from models.contract import Contract
from models.user import Review, User
from models import storage
from api.v1.views.token import requires_token

def calc_tot_rate(user_id):
    """Calculates and stores the rating avg of user"""
    user = storage.get(User, user_id)
    _session = storage.session()
    reviews = _session.query(Review).\
            filter(Review.for_user_id==user_id).all()
    total = 0
    count = 0
    for review in reviews:
        total += int(review.rating)
        count += 1
    try:
        rate_tot = total / count
    except:
        user.rating = total
        storage.save()
        return
    user.rating = rate_tot
    storage.save()

@api_views.route('/contracts/<contract_id>/rate',
           methods=['POST'], strict_slashes=False)
@requires_token
def rate_contract(user_id, contract_id):
    """Handles rating and review of contract by Buyer"""
    if not request.get_json():
        abort(400, 'Not a JSON')

    _session = storage.session()
    contract = _session.query(Contract).\
            filter(Contract.id==contract_id).first()
    if not contract:
        abort(404, 'Contract Not Found')
    if user_id == contract.buyer_id:
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
        return make_response(jsonify({'message': 'Rated and reviewes successfully'}), 200)
    return make_response(jsonify({'error': 'Error updating data'}), 501)

@api_views.route('/contracts/<contract_id>/initiate',
                 methods=['POST'], strict_slashes=False)
@requires_token
def initiate_con(user_id, contract_id):
    """Initiate contract by Seller, request => {"status": "ongoing"}"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'status' not in request.get_json().keys():
        abort(400, 'Invalid data')
    _session = storage.session()
    if not contract:
        abort(404, 'Contract Not Found')
    req = request.get_json()

    if user_id == contract.seller_id:
        for k, v in req.items():
            setattr(contract, k, v)
        storage.save()
        return make_response(jsonify({'message':\
                                      'Contract updated sucessfully'}), 200)
    else:
        abort(400, 'Login rquired')

@api_views.route('/contracts/<contract_id>', methods=['GET'],
                 strict_slashes=False)
@requires_token
def contract_view(user_id, contract_id):
    """View Contract by Seller or Buyer"""

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
@requires_token
def contract_create(user_id):
    """User create Contract as Buyer"""
    if not user_id:
        abort(400, 'Login required')
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
    s_user = _session.query(User).\
            filter(User.user_name==seller).first()
    b_user = _session.query(User).\
            filter(User.user_name==buyer).first()
    seller_id = s_user.id
    buyer_id = b_user.id
    if user_id != buyer_id:
        abort(400, 'Login required, unathorised')
    name = req['name']
    descr = req['desc']
    status = 'created'
    amount = float(req['amount'])

    new_contract = Contract(c_type=c_type, seller_id=seller_id,
                            buyer_id=buyer_id, name=name, description=descr,
                            status=status, amount=amount)
    storage.new(new_contract)
    storage.save()
    return make_response(jsonify({'messaege':\
            'Contract Created Successfully'}), 200)

@api_views.route('/contracts/<contract_id>/dispute',
                 methods=['POST'], strict_slashes=False)
@requires_token
def dispute_contract(user_id, contract_id):
    """Buyer(User) sets contract status to disputed and automatically
    send 0 rating review with issue as review"""
    if not request.get_json():
        abort(400, 'Not a JSON')

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
        return make_reponse(jsonify({'message':\
                'Dispute review sent successfully'}), 200)
    abort(500)

@api_views.route('/<user_name>/contracts', methods=['GET'], strict_slashes=False)
@requires_token
def get_contracts(user_id, user_name):
    _session = storage.session()
    user = _session.query(User).\
            filter(User.user_name==user_name).first()
    if user_id != user.id:
        abort(400, 'Not authorised')
    contracts_as_s = _session.query(Contract).\
            filter(Contract.seller_id==user.id).all()
    contracts_as_b = _session.query(Contract).\
            filter(Contract.buyer_id==user.id).all()
    as_s_list = []
    as_b_list = []
    for con in contracts_as_s:
        con = con.to_dict()
        user_as_b = _session.query(User).\
                filter(User.id==con['buyer_id']).first()
        user_as_s = _session.query(User).\
                filter(User.id==con['seller_id']).first()
        user_as_s = user_as_s.user_name
        user_as_b = user_as_b.user_name
        con['user_as_b'] = user_as_b
        con['user_as_s'] = user_as_s
        as_s_list.append(con)
    for con in contracts_as_b:
        con = con.to_dict()
        user_as_b = _session.query(User).\
                filter(User.id==con['buyer_id']).first()
        user_as_s = _session.query(User).\
                filter(User.id==con['seller_id']).first()
        user_as_s = user_as_s.user_name
        user_as_b = user_as_b.user_name
        con['user_as_b'] = user_as_b
        con['user_as_s'] = user_as_s
        as_b_list.append(con)

    all_dict = {'Contracts_buyer': as_b_list, 'Contract_seller': as_s_list}
    return make_response(jsonify(all_dict), 200)
