from flask import render_template
from . import deposits

# PUT THIS AT BOTTOM!
@deposits.route('/deposits_home')
def deposits_home():
    return render_template('deposits/deposits_home.html')
