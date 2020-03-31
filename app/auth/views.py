from flask import render_template, flash, redirect, url_for, request
from . import auth
from forms import RegistrationForm, LoginForm
from ..models import User, Queries
from flask_login import login_user, logout_user, current_user
from app import db


@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))
    form = RegistrationForm()
    username = form.username.data
    password = form.password.data
    if form.validate_on_submit():
        usrData = Queries().register(username, password)
        flash(f'Your account has been created. You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))
    form = LoginForm()
    username = form.username.data
    password = form.password.data
    userRemember = form.remember.data
    if form.validate_on_submit():
        usrData = Queries().login_checkUser(username, password)
        if usrData:
            user = User(usrData[0], usrData[1], usrData[2], usrData[3])
            login_user(user, remember=userRemember)
            next_page = request.args.get('next')
            flash('Welcome ' + username + '. You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home.homepage'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('auth/login.html', title='Login', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.homepage'))
