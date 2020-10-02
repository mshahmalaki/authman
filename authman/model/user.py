from datetime import datetime
from authman import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now())
    is_enabled = db.Column(db.Boolean, default=False)
