from flask import abort
from flask_restx import Resource
from authman.controller import UserController


class UserResource(Resource):
    def get(self, user_id=None):
        if user_id is None:
            return UserController.get_users()
        else:
            pass

    def post(self, user_id=None):
        if user_id is None:
            return UserController.create_user()
        else:
            abort(405)

    def patch(self, user_id=None):
        pass

    def delete(self, user_id=None):
        pass
