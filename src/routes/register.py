from argparse import Namespace


from flask import request
from flask_restx import Namespace, Resource
from models.user import User

api = Namespace('register')

@api.route('/')
class Register(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return {'error': 'bad request'}, 400
        data = request.get_json()

        username = data['username']
        password = data['password']
        email = data['email']
        phone = data['phone']
        name = data['name']
        
        User.create(username=username, password=password, name=name, email=email, phone=phone)
        return {'message': 'success'}, 200
