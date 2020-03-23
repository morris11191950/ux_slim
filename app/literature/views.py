from flask import render_template
from . import literature
from flask_login import login_required

# THIS MUST BE AT BOTTOM!
@literature.route('/literature')
@login_required
def literature():
    return render_template('literature/literature.html')
