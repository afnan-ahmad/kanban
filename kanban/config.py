import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECURITY_PASSWORD_HASH = None
    SECURITY_PASSWORD_SALT = None
    SECRET_KEY = None

    SECURITY_REGISTERABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False

    DEBUG = False


class DevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, '../db_directory')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(SQLITE_DB_DIR, 'kanban.sqlite3')

    # The values specified here are only to facilitate in running the app for demonstration purpose.
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'abc'
    SECRET_KEY = 'abc'

    SECURITY_REGISTERABLE = True

    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    SECURITY_PASSWORD_HASH = os.getenv('SECURITY_PASSWORD_HASH')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
    SECRET_KEY = os.getenv('SECRET_KEY')

    SECURITY_REGISTERABLE = True

    DEBUG = False
