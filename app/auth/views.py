from flask import render_template, flash, redirect, url_for, request
from . import auth
from app.auth.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from ..models import User, Queries
from flask_login import login_user, logout_user, current_user, login_required
from app import db, mail
from flask_mail import Message


@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))
    form = RegistrationForm()
    username = form.username.data
    password = form.password.data
    email = form.email.data
    if form.validate_on_submit():
        usrData = Queries().register(username, password, email)
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
            user = User(usrData[0], usrData[1], usrData[2], usrData[3], usrData[4])
            #print('userRemember ', userRemember)
            login_user(user, remember=userRemember)
            next_page = request.args.get('next')
            flash('Welcome ' + username + '. You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home.homepage'))
            #return redirect(next_page) if next_page else redirect(url_for('literature.literature'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('auth/login.html', title='Login', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.homepage'))

@auth.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        Queries().update_account(username, email)
        #Must add in here a routine to save to db!!!
        flash('Your account has been updated.', 'success')
        return redirect(url_for('auth.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('auth/account.html', title='Account', form=form)

def send_reset_email(user):
    token = user.get_reset_token()
    #print('token ', token)
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    #print('user.email ', user.email)
    #print('msg ', msg)
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
    #print('msg.body ', msg.body)

@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))
    form = RequestResetForm()
    if form.validate_on_submit():
        userData = Queries().reset_password_checkUser(form.username.data)
        #print('userData ', userData)
        user = User(userData[0], userData[1], userData[2], userData[3])
        #print('user ', user)
        send_reset_email(user)
        flash('An email has been sent with instructions to  reset your password', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_request.html', title='Reset Password', form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))
    print('token in reset ', token)
    user = User.verify_reset_token(token)
    print('user in reset ', user)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = Queries().update_password(user.username, form.password.data)
        flash(f'Your password has been updated. You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_token.html', title='Reset Password', form=form)
