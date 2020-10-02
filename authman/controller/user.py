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