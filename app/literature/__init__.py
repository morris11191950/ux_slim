from flask import Blueprint

literature = Blueprint('literature', __name__)

from . import views
