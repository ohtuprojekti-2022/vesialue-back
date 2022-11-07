import jwt
from flask import request
from flask_restx import Namespace, Resource
from werkzeug.exceptions import BadRequest
from bson.objectid import ObjectId
from services.inventory_service import inventory_service
from services.user_service import user_service
from models.user import User
from utils.config import SECRET_KEY

api = Namespace('inventory')


@api.route('')
class AddInventory(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {'error': 'bad request'}, 400
        data = request.get_json()

        user = user_service.check_authorization(request.headers)

        inventory = inventory_service.add_inventory(data, user)

        return inventory, 200

    def get(self):
        return inventory_service.get_all_inventories(), 200

@api.route('/edit')
class EditRequest(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {'error': 'bad request'}, 400
        data = request.get_json()

        user = user_service.check_authorization(request.headers)

        inventory = inventory_service.add_edited_inventory(data, user)

        return inventory, 200

    def get(self):
        return inventory_service.get_all_edited_inventories(), 200

@api.route('/edit/<string:report_id>')
class GetEdited(Resource):
    def get(self, report_id):
        inventory = inventory_service.get_edited_inventory(report_id)
        return inventory, 200

@api.route('/<string:report_id>')
class GetInventory(Resource):
    def get(self, report_id):
        inventory = inventory_service.get_inventory(report_id)
        return inventory, 200

@api.route('/areas')
class GetAreas(Resource):
    def get(self):
        return inventory_service.get_areas(), 200
