from os import environ


class Config:
    DEBUG = True if int(environ.get("AUTHMAN_DEBUG", "0")) else False
    ENV = environ.get("AUTHMAN_ENV", "production")
    SQLALCHEMY_DATABASE_URI =  environ.get("AUTHMAN_DATABASE_URI", None)
    SQLALCHEMY_TRACK_MODIFICATIONS = DEBUG
