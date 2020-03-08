from flask import Blueprint

trading_post = Blueprint('trading_post', __name__)

from . import views
