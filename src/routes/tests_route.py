from flask_restx import Namespace, Resource

api = Namespace('tests')


@api.route('/reset/')
class Tests(Resource):
    def post(self):
        # Reset database
        # ...
        return 'reset succeed', 200
