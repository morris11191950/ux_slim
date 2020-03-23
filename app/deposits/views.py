from flask import render_template
from . import deposits
from flask_login import login_required

# PUT THIS AT BOTTOM!
@deposits.route('/deposits_home')
@login_required
def deposits_home():
    return render_template('deposits/deposits_home.html')
