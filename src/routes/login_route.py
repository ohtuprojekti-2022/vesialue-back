from flask import request
from flask_restx import Namespace, Resource
from services.user_service import user_service

api = Namespace('login')

@api.route('')
class Login(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {'error': 'bad request'}, 400
        data = request.get_json()
        return user_service.login_user(data['username'], data['password']), 200
