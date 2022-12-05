from flask import request
from flask_restx import Namespace, Resource
from services.user_service import user_service

api = Namespace('user')

@api.route('/admin')
class SetAdmin(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {'error': 'bad request'}, 400
        data = request.get_json()
        if user_service.check_admin(request.headers):
            return user_service.set_admin(data['username'], data['admin_value']), 200
        return {'error': 'bad request'}, 400

@api.route('/edit')
class EditUser(Resource):
    def put(self):
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {'error': 'bad request'}, 400
        user_data = request.get_json()
        user = user_service.check_authorization(request.headers)
        return user_service.edit(user, user_data), 200

@api.route('/edit-password')
class EditPassword(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {'error': 'bad request'}, 400
        data = request.get_json()
        user = user_service.check_authorization(request.headers)
        return user_service.edit_password(user, data['current_password'], data['new_password']), 200
