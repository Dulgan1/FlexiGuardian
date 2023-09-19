from app_dynamics import app_views
from app_dynamics.auth import requires_token
from models import storage
from models.user import User, Review
from models.contract import Contract
from models.business import Business
from models.address import Address
import re
import random
import uuid
from werkzeug.security import generate_password_hash
from flask import (redirect, url_for,
                   session, flash,
                   request, render_template)

@app_views.route('/register', methods=['POST', 'GET'], strict_slashes=False)
def register():
    """ Handles new user registrations"""
    image_urls = ['https://i.ibb.co/vdPfRhw/FB-IMG-16876279408284166.jpg',
                  'https://i.ibb.co/khQzRqs/FB-IMG-16902292397886720.jpg',
                  'https://i.ibb.co/y0qRgry/FB-IMG-16893686181680673.jpg',
                  'https://i.ibb.co/ynCPC8x/J0c-JYQsuv-Ex-NOBs-A1v6t-1-m9c8x-2x.jpg',
                  'https://i.ibb.co/n1nbF6R/D3-UTUc3f-Zw-GYN4-KW4-TG6-1-f2cbk.jpg',
                  'https://i.ibb.co/GvZMVYm/1681229924028.jpg',
                  'https://i.ibb.co/kHkJv2b/1681228415670.jpg',
                  'https://i.ibb.co/XkGXtTp/1333154-600x600.jpg']

    if 'user_id' in session:
        flash('Already Registered and logged in')
        return redirect(url_for('app_views.home'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        user_name = request.form['user_name'].replace(" ", "")
        phone = request.form['phone']

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            error = 'Invalid email'
            return render_template('register.html', error=error)

        elif not re.match(r'[A-Za-z0-9]+', user_name):
            error = 'Invalid username, use only alphabets and numbers'
            return render_template('register.html', error=error)

        _session = storage.session()
        acct_exists = _session.query(User).\
                filter(User.email==email).first()
        if acct_exists:
            error = 'user with email already exists'
            return render_template('register.html', error=error)
        user_exists = _session.query(User).\
                filter(User.user_name==user_name).first()
        if user_exists:
            error = 'username is taken'
            return render_template('register.html', error=error)
        else:
            if request.form['password'] == request.form['cpassword']:
                password = generate_password_hash(request.form['password'], method='md5')
            else:
                error = 'password not matched'
                return render_template('register.html', error=error)
            new_user = User(name=name, email=email,
                            user_name=user_name,phone=phone,
                            password=password, image_url=random.choice(image_urls))

            storage.new(new_user)
            storage.save()
            session['user_id'] = new_user.id
            session['user_name'] = new_user.user_name
            flash('Your account is successfully registered')
            return redirect(url_for('app_views.home'))
    return render_template('register.html')

@app_views.route('/users/<user_name>/business',
                 methods=['GET', 'POST'], strict_slashes=False)
@requires_token
def register_business(user_id, user_name):
    """ Handles new business registration """
    _session = storage.session()
    user_byun = _session.query(User).filter(User.user_name==user_name).first()
    user_byid = _session.query(User).filter(User.id==user_id).first()

    if user_id == user_byun.id:
        if request.method == 'POST':
            if user_byid.business_name:
                flash('Can not register another Business')
                return redirect(url_for('app_views.profile',
                                        user_name=user_name))
            name = request.form['name']
            contacts = request.form['contacts']
            description = request.form['description']
            state = request.form['state']
            zipcode = request.form['zipcode']
            addr_line = request.form['addr_line']

            business = Business(user_id=user_id, name=name,
                                contacts=contacts, description=description)
            address = Address(state=state, zipcode=zipcode, business_id=business.id,
                              addr_line=addr_line)
            user_byun.business_name = business.name
            storage.new(business)
            storage.new(business)
            user_byun.save()
            storage.save()
            flash('Business profile created successfully')
            return redirect(url_for('app_views.profile', user_name=user_name))
        else:
            return render_template('business.html', user=user_byid)
@app_views.route('/users/<user_name>', methods=['GET'], strict_slashes=False)
def profile(user_name):
    """ Handles user profile view"""
    _session = storage.session()
    user = _session.query(User).filter(User.user_name==user_name).first()
    business = _session.query(Business).\
            filter(Business.user_id==user.id).first()
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
    if 'user_id' in session:
        if session['user_id'] == user.id:
            return render_template('dashboard.html', user_name=user_name,
                                   logged_user=user, business=business,
                                   cache_id=uuid.uuid4(),
                                   contracts_as_b=as_b_list,
                                   contracts_as_s=as_s_list)
    reviews = _session.query(Review).\
            filter(Review.for_user_id==user.id).all()
    return render_template('user.html', user_name=user_name,
                           business=business, user=user,
                           cache_id=uuid.uuid4(), reviews=reviews)
