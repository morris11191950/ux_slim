from flask import Flask
from flaskext.mysql import MySQL
from config import Config

db = MySQL()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
