from flask import render_template
from . import trading_post

@trading_post.route('/trading_post')
def trading_post():
    return render_template('trading_post/trading_post.html')
