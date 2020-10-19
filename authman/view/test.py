from flask_restx import Resource


class TestResource(Resource):

    def get(self):
        return {"test": "ok"}
