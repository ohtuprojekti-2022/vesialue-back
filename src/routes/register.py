from flask import request
from flask_restx import Namespace, Resource
from services.user_service import create_user
from utils.config import SECRET_KEY
import jwt

api = Namespace('register')

@api.route('/')
class Register(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return {'error': 'bad request'}, 400
        user = create_user(request.get_json())

        token = jwt.encode({'user_id': user['id']}, SECRET_KEY)
        return {'login_token': token}, 200
