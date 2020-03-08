from flask import render_template
from . import maps

@maps.route('/maps_home')
def maps_home():
    return render_template('maps/maps_home.html')
