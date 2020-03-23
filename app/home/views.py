from flask import render_template
from . import home

@home.route('/', methods=('GET', 'POST'))
@home.route('/homepage')
def homepage():
    return render_template('home/homepage.html')
