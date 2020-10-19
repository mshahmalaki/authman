from flask_restx import Resource


class TestResource(Resource):

    def get(self):
        return jsonify({"test": "ok"})
