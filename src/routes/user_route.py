from flask import request
from flask_restx import Namespace, Resource
from services.user_service import set_admin

api = Namespace('admin')

@api.route('')
class SetAdmin(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {'error': 'bad request'}, 400
        data = request.get_json()
        return set_admin(data['username'], data['admin_value']), 200
