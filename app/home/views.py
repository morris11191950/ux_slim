from flask import render_template, session
from . import home

@home.route('/')
def homepage():
    return render_template('home/homepage.html')
