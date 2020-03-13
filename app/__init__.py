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

    from .literature import literature as literature_blueprint
    app.register_blueprint(literature_blueprint)

    from .deposits import deposits as deposits_blueprint
    app.register_blueprint(deposits_blueprint)

    from .maps import maps as maps_blueprint
    app.register_blueprint(maps_blueprint)

    from .trading_post import trading_post as trading_post_blueprint
    app.register_blueprint(trading_post_blueprint)

    from .prospects import prospects as prospects_blueprint
    app.register_blueprint(prospects_blueprint)

    return app
