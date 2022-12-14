from flask import request
from flask_restx import Namespace, Resource
from services.user_service import user_service

api = Namespace('login')

@api.route('')
class Login(Resource):
    """Log in route.
    post:
        summary: Endpoint for logging a user in.
        description: Generates an authentication token. Returns token and
            user schema.
        responses:
            200:
                description: Returns authentication token
                    and user schema as dict.
            400:
                description: Bad request.
    """
    def post(self):
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {'error': 'bad request'}, 400
        data = request.get_json()
        return user_service.login_user(data['username'], data['password']), 200
