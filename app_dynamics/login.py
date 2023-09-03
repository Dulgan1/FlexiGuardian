#!/usr/bin/python
from app_dynamics import app_views
from flask import session, flash, request, render_template
from models import storage
from models.user import User
from werkzeug.security import check_password_hash
""" Route Login """

@app_views.route('/home', strict_slashes=False)
@app_views.route('/')
def home():
    if 'user_id' in session:
        return render_template('index2.html')
    return render_template('index.html')


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
                return redirect(url_for('home'))

            error = 'Invalid email or password'
            return render_template('login.html', error=error)
    return render_template('login.html')
