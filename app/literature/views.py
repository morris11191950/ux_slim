from flask import render_template
from . import literature

# THIS MUST BE AT BOTTOM!
@literature.route('/literature')
def literature():
    return render_template('literature/literature.html')
