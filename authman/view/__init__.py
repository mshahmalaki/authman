from authman import api
from authman.view.user import UserResource


api.add_resource(
    UserResource,
    "/users",
    methods=["GET", "POST"]
)
api.add_resource(
    UserResource,
    "/users/<int:user_id>",
    methods=["GET", "PATCH", "DELETE"]
)