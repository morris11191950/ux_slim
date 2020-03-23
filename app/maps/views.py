from flask import render_template
from . import maps
from flask_login import login_required

@maps.route('/maps_home')
@login_required
def maps_home():
    return render_template('maps/maps_home.html')
