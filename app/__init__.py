from sys import prefix
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import unittest
csrf = CSRFProtect()
db = SQLAlchemy()
DB_NAME = "database.sqlite3"



def create_app():

    app = Flask(__name__, static_url_path='/static')

    app.config['SECRET_KEY'] = "THISWASSUPPOSEDTOBEASECRET"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////mnt/f/data and algo/IITMadras/app-dev/MyTicket2.0/myticket2/app/myticketDB.db"
    app.config['TESTING'] = True
    client = app.test_client()

    db.init_app(app)
    from .controllers import controllers
    from .auth import auth, login_manager
    from .admin_controllers import admin_controls, bootstrap
    app.register_blueprint(controllers, prefix='/')
    app.register_blueprint(auth, prefix='/')
    app.register_blueprint(admin_controls, prefix='/')
    bootstrap.init_app(app)
    from .models import User
    app.app_context().push()
    create_database(app)
    # users configurations
    login_manager.init_app(app)
    login_manager.login_view = 'auth.user_login'
    csrf.init_app(app)
    # admin configurations

    return app


def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all()
        print('Created Database!')
