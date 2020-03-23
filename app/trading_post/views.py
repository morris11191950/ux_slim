from flask import render_template
from . import trading_post
from flask_login import login_required

@trading_post.route('/trading_post')
@login_required
def trading_post():
    return render_template('trading_post/trading_post.html')
