from flask import Flask
from flaskext.mysql import MySQL
from config import Config
from flask_login import LoginManager
from flask_mail import Mail
from flask_cors import CORS

db = MySQL()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

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
