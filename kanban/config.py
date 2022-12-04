import os

from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECURITY_PASSWORD_HASH = None
    SECURITY_PASSWORD_SALT = None
    SECRET_KEY = None

    JWT_SECRET_KEY = None
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

    SECURITY_REGISTERABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False

    WTF_CSRF_ENABLED = False

    DEBUG = False


class DevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, '../db_directory')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(SQLITE_DB_DIR, 'kanban.sqlite3')

    # The values specified here are only to facilitate in running the app for demonstration purpose.
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'nXweJD@T4uZa3aZeWxHiQw73'
    SECRET_KEY = 'kWNQjF9XJxW8B8A78$veSQ5P'

    JWT_SECRET_KEY = 'AQ8lgJ@Gu93gGQRnKNu3fbcI'

    SECURITY_REGISTERABLE = True

    WTF_CSRF_ENABLED = False

    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    SECURITY_PASSWORD_HASH = os.getenv('SECURITY_PASSWORD_HASH')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
    SECRET_KEY = os.getenv('SECRET_KEY')

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    SECURITY_REGISTERABLE = True

    WTF_CSRF_ENABLED = False

    DEBUG = False
