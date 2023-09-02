from app_dynamics import app_views
from app_dynamics.auth import requires_token
from models import storage
from models.user import User
import re
from werkzeug.security import generate_password_hash
from flask import (redirect, url_for,
                   session, flash,
                   request, render_template)

@app_views.route('/register', methods=['POST', 'GET'], strict_slashes=False)
def register():
    """ Handles new user registrations"""

    if 'user_id' in session:
        flash('Already Registered and logged in')
        return redirect(url_for('home'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        user_name = request.form['user_name']
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
            password = generate_password_hash(request.form['password'], method='md5')
            new_user = User(name=name, email=email,
                            user_name=user_name,phone=phone,
                            password=password)

            storage.new(new_user)
            storage.save()
            session['user_id'] = new_user.id
            session['user_name'] = new_user.user_name
            flash('Youe account is successfully registered')
            return redirect(url_for('home'))
    return render_template('register.html')

@app_views.route('/users/<user_name>/business',
                 methods=['GET', 'POST'], strict_slashes=False)
@requires_token
def register_business(user_id, user_name):
    _session = storage.session()
    user_byun = _session.query(User).filter(User.user_name==user_name).first()

    if user_id == user_byun.id:
        if request.method == 'POST':
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
            storage.new(business)
            storage.new(business)
            storage.save()
            flash('Business profile created successfully')
            return redirect(url_for('/users/' + user_name))
        else:
            whose = 'owner'
            return render_template('business.html', whose=whose)
    else:
        if request.method == 'GET':
            whose = 'not owner'
            return render_template('business.html', whose=whose)
        else:
            flash('Can not create business profile for user')
            return redirect(url_for('/'))

@app_views.route('/users/<user_name>', methods=['GET'], strict_slashes=False)
def profile(user_name): #TODO: MAKE SURE TO COMPLETE user.js and dashboard.js
    _session = storage.session()
    user = _session.query(User).filter(User.user_name==user_name).first()

    if 'user_id' in session:
        if session['user_id'] == user.id:
            return render_template('dashboard.html', user_name=user_name)
    return render_template('user.html', user_name=user_name)