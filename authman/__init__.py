from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from authman.config import Config


db = SQLAlchemy()
mg = Migrate()
ma = Marshmallow()
api = Api()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    return app

