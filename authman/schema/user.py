from authman import ma
from authman.model import User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field()
    password = ma.auto_field(load_only=True)
    created_at = ma.auto_field(dump_only=True)
    is_enabled = ma.auto_field()
