from flask import request, abort
from authman import db
from authman.model import User
from authman.schema import UserSchema


class UserController:
    def get_users():
        users = User.query.all()
        users_schema = UserSchema(many=True)
        return {
            "users": users_schema.dump(users)
        }

    def get_user(user_id):
        user= User.query.get(user_id)
        if user is None:
            abort(404)
        else:
            user_schema = UserSchema()
            return {
                "user": user_schema.dump(user)
            }

    def create_user():
        if request.is_json is False:
            abort(415)
        json_data = request.get_json()
        user_schema = UserSchema()
        try:
            data = user_schema.load(json_data)
        except:
            abort(400)
        user = User.query.filter_by(username=data["username"]).first()
        if user is not None:
            abort(409)
        user = User(username=data["username"], password=data["password"])
        db.session.add(user)
        db.session.commit()
        return {
            "user": user_schema.dump(user)
        }

    def update_user(user_id):
        if request.is_json is False:
            abort(415)
        json_data = request.get_json()
        user_schema = UserSchema(only=["password"])
        try:
            data = user_schema.load(json_data)
        except:
            abort(400)
        user = User.query.get(user_id)
        if user is None:
            abort(404)
        user.password = data["password"]
        db.session.commit()
        user_schema = UserSchema()
        return {
            "user": user_schema.dump(user)
        }
