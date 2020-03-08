from flask import Blueprint

deposits = Blueprint('deposits', __name__)

from . import views
