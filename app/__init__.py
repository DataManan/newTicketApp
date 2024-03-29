from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_wtf.csrf import CSRFProtect
import unittest
from .config import LocalDevelopmentConfig
csrf = CSRFProtect()
db = SQLAlchemy()
DB_NAME = "myticketDB.db"



def create_app():

    app = Flask(__name__, static_url_path='/static', template_folder='templates')

    app.config.from_object(LocalDevelopmentConfig)
    app.config['TESTING'] = True
    client = app.test_client()

    db.init_app(app)
    # api = Api(app)
    from .controllers.users.controllers import controllers
    from .controllers.auth import auth, login_manager
    from .controllers.admin.admin_controllers import admin_controls, bootstrap
    from .controllers.users.full_text_search import fts, fts_search

    fts_search.init_app(app)

    app.register_blueprint(controllers, prefix='/')
    app.register_blueprint(auth, prefix='/')
    app.register_blueprint(admin_controls, prefix='/admin')
    app.register_blueprint(fts, prefix='/search')

    bootstrap.init_app(app)

    app.app_context().push()
    create_database(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.user_login'
    csrf.init_app(app)
    
    return app


def create_database(app):
    if not path.exists('app/database' + DB_NAME):
        db.create_all()
        print('Database Created!')

# app, api = create_app()

