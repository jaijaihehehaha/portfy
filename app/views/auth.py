from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..models import User
from .. import db, login_manager
from flask_login import login_user, logout_user, login_required, current_user


auth_bp = Blueprint('auth', __name__, url_prefix='')


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']


        if User.query.filter((User.username==username) | (User.email==email)).first():
            flash('Username or email already exists', 'danger')
            return redirect(url_for('auth.signup'))


        user = User(username=username, email=email, display_name=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Account created. Please log in.', 'success')
        return redirect(url_for('auth.login'))


    return render_template('auth/signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter((User.username==username) | (User.email==username)).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in', 'success')
            return redirect(url_for('dash.dashboard'))
        flash('Invalid credentials', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('public.index'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))