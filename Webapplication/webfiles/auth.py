from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from password_strength import PasswordPolicy
from password_strength import PasswordStats
from flask import current_app as app

auth = Blueprint('auth', __name__)

policy = PasswordPolicy.from_names(
    length=8,
    uppercase=1, 
    numbers=1, 
    strength=0.66
)

limiter = Limiter(app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

@auth.route('/login', methods=['GET', 'POST'])
@limiter.limit('3 per day')
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        stats = PasswordStats(password1)
        checkpolicy = policy.test(password1)

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif stats.strength() < 0.30:
            print(stats.strength())
            flash("Password not strong enough. Avoid consecutive characters and easily guessed words")

        else:
            print(stats.strength())
            new_user = User(email=email, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Your account has successfully been created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
