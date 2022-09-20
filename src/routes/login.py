from flask import request
from flask_restx import Namespace, Resource
from services.user_service import login_user, generate_token
from utils.config import SECRET_KEY
import jwt

api = Namespace('login')

@api.route('/')
class Login(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {'error': 'bad request'}, 400
        user = login_user(request.get_json())
        token = generate_token(user)
        return {'auth': token}, 200
