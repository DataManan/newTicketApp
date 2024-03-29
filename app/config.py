import os

# setting up base dir
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)) + "/database")
    # print(SQLITE_DB_DIR)
    SECRET_KEY = "THISWASSSUPPOSEDTOBEASECRET"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "myticketDB.db")
    DEBUG = True
