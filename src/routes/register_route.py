from flask import request
from flask_restx import Namespace, Resource
from services.user_service import user_service

api = Namespace('register')

@api.route('')
class Register(Resource):
    """Register route.
    post:
        summary: Endpoint for registering a new user.
        description: Creates new user based on data received
            from frontend.
        responses:
            200:
                description: Creates new user and logs the new user in.
                    Returns authentication token and user schema as dict.
            400:
                description: Bad request.
    """
    def post(self):
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {'error': 'bad request'}, 400
        data = request.get_json()
        user = user_service.create_user(data)
        return user_service.login_user(user['username'], data['password']), 200
