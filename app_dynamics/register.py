from app_dynamics import app_views
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
            return render_template('login.html', error=error)

        elif not re.match(r'[A-Za-z0-9]+', user_name):
            error = 'Invalid username, use only alphabets and numbers'
            return render_template('login.html', error=error)

        _session = storage.session()
        acct_exists = _session.query(User).\
                filter(User.email==email).first()
        elif acct_exists:
            error = 'user with email already exists'
            return render_template('login.html', error=error)
        user_exists = _session.query(User).\
                filter(User.user_name==user_name).first()
        elif user_exists:
            error = 'username is taken'
            return render_template('login.html', error=error)
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
