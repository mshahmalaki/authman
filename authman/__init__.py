from flask import Flask
from flask.cli import AppGroup
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from healthcheck import HealthCheck

from authman.config import Config


db = SQLAlchemy()
mg = Migrate()
ma = Marshmallow()
api = Api()


app_cli = AppGroup("app", help="Application related commands.")


from authman import model
from authman import view
from authman import command


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mg.init_app(app, db)
    ma.init_app(app)
    api.init_app(app)
    app.cli.add_command(app_cli)

    health = HealthCheck(app, "/status")
    health.add_check(command.db_check)

    return app
