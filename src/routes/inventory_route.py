from flask import request
from flask_restx import Namespace, Resource
from services.inventory_service import inventory_service

api = Namespace('inventory')


@api.route('/')
class AddInventory(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {'error': 'bad request'}, 400
        data = request.get_json()
        inventory = inventory_service.add_inventory(data)

        return inventory, 200
    
    def get(self):
        return inventory_service.get_all_inventories()

