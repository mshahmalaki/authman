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

    def create_user():
        if request.is_json:
            json_data = request.get_json()
            user_schema = UserSchema()
            try:
                data = user_schema.load(json_data)
            except:
                abort(400)
            user = User(username=data["username"], password=data["password"])
            db.session.add(user)
            db.session.commit()
            return {
                "user": user_schema.dump(user)
            }
        else:
            abort(415)

