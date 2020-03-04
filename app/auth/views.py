import functools
from flask import render_template, request, g, session, redirect, url_for, flash
from . import auth
from werkzeug.security import check_password_hash, generate_password_hash

from app import db

@auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username_ = request.form['username']
        password = request.form['password']
        conn = db.connect()
        cursor = conn.cursor()

        error = None

        sql = "SELECT * FROM user WHERE username = '" + username_ + "' "

        cursor.execute(sql)

        data = cursor.fetchone()

        if data is None:
            error = 'Incorrect username.'
        elif not check_password_hash(data[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = data[0]
            return redirect(url_for('home.homepage'))

        flash(error)

    return render_template('auth/login.html')

@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    conn = db.connect()
    cursor = conn.cursor()

    if user_id is None:
        g.user = None
        #g.db_to_use = 'SJM_auth'
    else:
        sql = "SELECT * FROM user WHERE id = '" + str(user_id) + "' "
        cursor.execute(sql)
        data = cursor.fetchone()
        g.user = data[0]
        #g.db_to_use = 'SJM_suth'


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.homepage'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            #g.db_to_use = 'SJM_auth'
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
