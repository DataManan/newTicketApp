from sys import prefix
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
# from app.config import LocalDevelopmentConfig /mnt/f/data and algo/IITMadras/app-dev/MyTicket2.0/myticket2/templates

db = SQLAlchemy()
DB_NAME = "database.sqlite3"


def create_app():

    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////mnt/f/data and algo/IITMadras/app-dev/MyTicket2.0/myticket2/app/database.sqlite3"
    db.init_app(app)
    from .controllers import controllers

    app.register_blueprint(controllers, prefix='/')

    from .models import User
    app.app_context().push()
    create_database(app)

    return app


def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all()
        print('Created Database!')
