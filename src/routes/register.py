from flask import request
from flask_restx import Namespace, Resource
from services.user_service import create_user, login_user

api = Namespace('register')

@api.route('/')
class Register(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {'error': 'bad request'}, 400
        data = request.get_json()
        user = create_user(data)
        return login_user(user['username'], data['password']), 200
