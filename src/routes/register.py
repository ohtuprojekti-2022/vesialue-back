from flask import request
from flask_restx import Namespace, Resource
from services.user_service import create_user

api = Namespace('register')

@api.route('/')
class Register(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return {'error': 'bad request'}, 400
        user = create_user(request.get_json())
        return user, 200
