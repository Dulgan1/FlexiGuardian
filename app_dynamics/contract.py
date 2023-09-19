#!/usr/bin/python3
"""Handles routes for contract"""
from app_dynamics import app_views
from app_dynamics.auth import requires_token
from flask import (redirect, session,
                   request, render_template,
                   flash, url_for)
from models.contract import Contract
from models.user import Review, User
from models import storage

def calc_tot_rate(user_id):
    """Calculates and stores the rating avg of user"""
    user = storage.get(User, user_id)
    _session = storage.session()
    reviews = _session.query(Review).filter(Review.for_user_id==user_id).all()
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
    rate_tot = round(rate_tot, 2)
    user.rating = rate_tot
    storage.save()

@app_views.route('/contracts/<contract_id>/rate',
           methods=['GET', 'POST'], strict_slashes=False)
@requires_token
def rate_contract(user_id, contract_id):
    """Rating and review of contract by Buyer"""
    _session = storage.session()
    contract = _session.query(Contract).\
            filter(Contract.id==contract_id).first()
    if request.method == 'POST':
        if not contract:
            error = 'No such contract'
            return render_template('dashboard.html', error=error)
        if user_id == contract.buyer_id:
            rate = request.form['rate']
            review = request.form['review']
            if not rate and not review:
                error = 'Can not submit empty'
                return render_template('contractrate.html', error=error)
            rate = int(rate)
            seller_id = contract.seller_id

            new_review = Review(by_user_id=user_id,
                                for_user_id=seller_id,
                                review_body=review, rating=rate)
            storage.new(new_review)
            contract.review_id = new_review.id
            storage.save()
            calc_tot_rate(seller_id)
            flash('Review submitted successfully')
            return redirect(url_for('app_views.contract_view',
                                    contract_id=contract_id))
        error = 'Can not update data, not a participant'
        return render_template('dashboard.html', error=error)
    return render_template('contractrate.html', contract=contract)

@app_views.route('/contracts/<contract_id>', methods=['GET'],
                 strict_slashes=False)
@requires_token
def contract_view(user_id, contract_id):
    """View Contract by Seller or Buyer"""

    _session = storage.session()
    logged_user = _session.query(User).filter(User.id==user_id).first()
    contract = _session.query(Contract).\
            filter(Contract.id==contract_id).first()
    if not contract:
        flash('Contract Not Found')
        return redirect(url_for('app_views.home'))
    if contract.seller_id == user_id or contract.buyer_id == user_id:
        buyer = _session.query(User).\
                filter(User.id==contract.buyer_id).first()
        buyer_un = buyer.user_name
        seller = _session.query(User).\
                filter(User.id==contract.seller_id).first()
        seller_un = seller.user_name
        review = _session.query(Review).\
                filter(Review.id==contract.review_id).first()
        return render_template('contract.html', contract_id=contract.id,
                               contract_name=contract.name,
                               buyer_un=buyer_un, seller_un=seller_un,
                               description=contract.description,
                               contract_status=contract.status,
                               contract_amount=contract.amount,
                               contract_d=contract.disputed,
                               contract_type=contract.c_type,
                               contract_create_date=contract.created_at,
                               contract_update_date=contract.updated_at,
                               logged_user=logged_user.user_name,
                               review=review)
    else:
        flash('Unaccessible Contract')
        return redirect(url_for('app_views.home'))
@app_views.route('/users/<user_name>/contracts/create',
                 methods=['GET', 'POST'], strict_slashes=False)
@requires_token
def contract_create(user_id, user_name):
    """ Creates a contract """
    if request.method == 'POST':
        r_keys = ['c_type', 'name', 'desc', 'amount']

        for key in r_keys:
            if key not in request.form:
                error = 'Can not submit blank'
                return render_template('create_con.html', error=error)
        _session = storage.session()
        c_type = request.form['c_type']
        seller = user_name
        s_user = _session.query(User).filter(User.user_name==seller).first()
        seller_id = s_user.id
        buyer_id = user_id
        name = request.form['name']
        descr = request.form['desc']
        status = 'created'
        amount = float(request.form['amount'])

        new_contract = Contract(c_type=c_type, seller_id=seller_id,
                                buyer_id=buyer_id,
                                name=name, description=descr,
                                status=status, amount=amount)
        storage.new(new_contract)
        storage.save()
        flash('Contract created successfully')
        return redirect(url_for('app_views.contract_view', contract_id=new_contract.id))
    return render_template('create_con.html', user_name=user_name)

@app_views.route('/<user_name>/contracts', methods=['GET'],
                 strict_slashes=False)
@requires_token
def get_contracts(user_id, user_name):
    """ Handles contract viewing and interactions """
    _session = storage.session()
    user = _session.query(User).filter(User.user_name==user_name).first()
    contracts_as_s = _session.query(Contract).\
            filter(Contract.seller_id==user.id).all()
    contracts_as_b = _session.query(Contract).\
            filter(Contract.buyer_id==user.id).all()
    return render_template('404.html')

@app_views.route('/contracts/<contract_id>/dispute',
                 methods=['GET'], strict_slashes=False)
@requires_token
def dispute_contract(user_id, contract_id):
    """ Disputing a contract and automatic 0 rating """
    _session = storage.session()
    contract = _session.query(Contract).\
            filter(Contract.id==contract_id).first()
    if not contract:
        return render_template('404.html')
    if user_id == contract.buyer_id:
        note = 'Unsatisfied and disputed'
        review = Review(by_user_id=user_id, for_user_id=contract.seller_id,
                        review_body=note, rating=0)
        contract.disputed = 1
        contract.status = 'disputed'
        contract.review_id = review.id
        storage.new(review)
        storage.save()
        return redirect(url_for('app_views.contract_view',
                                contract_id=contract_id))

@app_views.route('/contracts/<contract_id>/initiate',
                 methods=['GET'], strict_slashes=False)
@requires_token
def initiate_con(user_id, contract_id):
    """Initiates tge contract by seller only """
    _session = storage.session()
    user = _session.query(User).\
            filter(User.id==user_id).first()
    contract = _session.query(Contract).\
            filter(Contract.id==contract_id).first()
    if not contract:
        return render_template('404.html')

    if user_id == contract.seller_id:
        contract.status = 'ongoing'
        storage.save()
        return redirect(url_for('app_views.profile',
                                user_name=user.user_name))
    else:
        return redirect(url_for('app_views.profile',
                                user_name=user.user_name))

@app_views.route('/contracts/<contract_id>/cancel',
                 methods=['GET'], strict_slashes=False)
@requires_token
def cancel_con(user_id, contract_id):
    """ Cancelling a contract """
    _session = storage.session()
    user = _session.query(User).filter(User.id==user_id).first()
    contract = _session.query(Contract).\
            filter(Contract.id==contract_id).first()
    if not contract:
        return render_template('404.html')
    if user_id == contract.buyer_id:
        contract.status = 'cancelled'
        storage.save()
        return redirect(url_for('app_views.profile',
                                user_name=user.user_name))
    else:
        return redirect(url_for('app_views.profile',
                                user_name=user.user_name))

@app_views.route('/contracts/<contract_id>/close',
                 methods=['GET'], strict_slashes=False)
@requires_token
def close_con(user_id, contract_id):
    """ Closing a contract """
    _session = storage.session()
    user = _session.query(User).filter(User.id==user_id).first()
    contract = _session.query(Contract).\
                         filter(Contract.id==contract_id).first()
    if not contract:
        return render_template('404.html')
    if user_id == contract.buyer_id:
        contract.status = 'closed'
        storage.save()
        return redirect(url_for('app_views.profile',
                                user_name=user.user_name))
    else:
        return redirect(url_for('app_views.profile',
                                user_name=user.user_name))
