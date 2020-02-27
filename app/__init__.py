from flask import Flask
#from flaskext.mysql import MySQL
#from config import Config

# print("I am in app __init__.py")

#db = MySQL()

def create_app():
    app = Flask(__name__)
    #app.config.from_object(Config)

    #db.init_app(app)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app
