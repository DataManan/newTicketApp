from sys import prefix
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager
from flask_admin import Admin
# from app.config import LocalDevelopmentConfig /mnt/f/data and algo/IITMadras/app-dev/MyTicket2.0/myticket2/templates

db = SQLAlchemy()
DB_NAME = "database.sqlite3"


def create_app():

    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = "THISWASSUPPOSEDTOBEASECRET"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////mnt/f/data and algo/IITMadras/app-dev/MyTicket2.0/myticket2/app/database.sqlite3"
    db.init_app(app)
    from .controllers import controllers
    from .auth import auth
    from .admin_controllers import admin_controls
    app.register_blueprint(controllers, prefix='/')
    app.register_blueprint(auth, prefix='/')
    app.register_blueprint(admin_controls, prefix='/')

    from .models import User
    app.app_context().push()
    create_database(app)
    # users configurations
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.user_login'
    # admin configurations
    # admin = Admin(app)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))




    return app


def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all()
        print('Created Database!')
