from flask import abort
from flask_restx import Resource
from authman.controller import UserController


class UserResource(Resource):
    def get(self, user_id=None):
        """
        GET /users --> List all users. GET /users/<user_id> --> List single user.
        """
        if user_id is None:
            return UserController.get_users()
        else:
            return UserController.get_user(user_id)

    def post(self, user_id=None):
        """
        POST /users --> Create new user.
        """
        if user_id is None:
            return UserController.create_user()
        else:
            abort(405)

    def patch(self, user_id=None):
        """
        PATCH /users/<user_id> --> Update user.
        """
        pass

    def delete(self, user_id=None):
        """
        DELETE /users/<user_id> --> Delete user.
        """
        pass
