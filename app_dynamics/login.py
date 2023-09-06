#!/usr/bin/python
from app_dynamics import app_views
from app_dynamics.auth import requires_token
from flask import (session, flash,
                   request, render_template, 
                   redirect, url_for)
from models import storage
from models.user import User
from werkzeug.security import check_password_hash
""" Route Login """


@app_views.route('/home', strict_slashes=False)
@app_views.route('/')
def home():
    _session = storage.session()
    users = _session.query(User).order_by(User.rating.desc()).all()
    if 'user_id' in session:
        logged_user = _session.query(User).\
                filter(User.id==session['user_id']).first()
        return render_template('index2.html', users=users, logged_user=logged_user)
    return render_template('index.html', users=users)


@app_views.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
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
    try:
        session.pop('user_id')
        session.pop('user_name')
    except:
        return redirect(url_for('app_views.home'))
    return redirect(url_for('app_views.login'))
