import jwt
from flask import request
from flask_restx import Namespace, Resource
from werkzeug.exceptions import BadRequest
from bson.objectid import ObjectId
from services.inventory_service import inventory_service
from models.user import User
from utils.config import SECRET_KEY

api = Namespace('inventory')


@api.route('/')
class AddInventory(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {'error': 'bad request'}, 400
        data = request.get_json()

        user = None
        if 'Authorization' in request.headers:
            token = str.replace(str(request.headers['Authorization']), 'Bearer ', '')
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            if not decoded_token['user_id']:
                raise BadRequest(description='Authorization token missing or invalid')
            user = User.objects.get({'_id': ObjectId(decoded_token['user_id'])})

        inventory = inventory_service.add_inventory(data, user)

        return inventory, 200

@api.route('/<string:report_id>')
class GetInventory(Resource):
    def get(self, report_id):
        inventory = inventory_service.get_inventory(report_id)
        return inventory, 200
