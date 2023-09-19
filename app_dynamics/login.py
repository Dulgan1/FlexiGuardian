""" Module for Login and authentication """
from app_dynamics import app_views
from app_dynamics.auth import requires_token
from flask import (session, flash,
                   request, render_template, 
                   redirect, url_for)
from models import storage
from models.user import User
from models.business import Business
from werkzeug.security import check_password_hash


@app_views.route('/home', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/', methods=['GET', 'POST'], strict_slashes=False)
def home():
    """ Loads home page, both for non-login and logged in"""
    if request.method == 'GET':
        _session = storage.session()
        users = _session.query(User).order_by(User.rating.desc()).all()
        if 'user_id' in session:
            logged_user = _session.query(User).\
                    filter(User.id==session['user_id']).first()
            return render_template('index2.html',
                                   users=users, logged_user=logged_user)
        return render_template('index.html', users=users)
    elif request.method == 'POST':
        squery = request.form['query']
        users = search(squery)
        if 'user_id' in session:
            logged_user = _session.query(User).\
                    filter(User.id==session['user_id']).first()
            return render_template('index2.html',
                                   users=users, logged_user=logged_user)
        return render_template('index.html', users=users)

@app_views.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """ Handles user login """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = storage.get_user(email)

        if not user:
            error = 'Invalid email or password '
            return render_template('login.html', error=error)
        else:
            user_id = user.id
            user = storage.get(User, user_id)

            if check_password_hash(user.password, password):
                session['user_id'] = user_id
                session['user_name'] = user.user_name
                flash('Successfully logged in')
                return redirect(url_for('app_views.home'))

            error = 'Invalid email or password'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app_views.route('/logout', methods=['GET'], strict_slashes=False)
def logout():
    """ Logging out of the app """
    try:
        session.pop('user_id')
        session.pop('user_name')
    except:
        return redirect(url_for('app_views.home'))
    return redirect(url_for('app_views.login'))

def search(squery):
    _session = storage.session()
    userss = _session.query(User).\
            filter(User.name.like('%{}%'.format(squery))).all()
    users_u = _session.query(User).\
            filter(User.user_name.like('%{}%'.format(squery))).all()
    userss.append(users_u)
    businesses = _session.query(Business).\
            filter(Business.name.like('%{}%'.format(squery))).all()
    busi_desc = _session.query(Business).\
            filter(Business.description.like('%{}%'.format(squery))).all()
    for business in businesses:
        user = _session.query(User).\
                filter(User.id==business.user_id).first()
        userss.append(user)
    for business in busi_desc:
        user = _session.query(User).\
                filter(User.id==business.user_id).first()
        userss.append(user)

    users = []

    for user in userss:
        if user not in users:
            users.append(user)
    return users
