from argparse import Namespace
from flask import request
from flask_restx import Namespace, Resource
from services.inventory_service import add_inventory

api = Namespace('add_inventory')


@api.route('/')
class AddInventory(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {'error': 'bad request'}, 400
        data = request.get_json()
        inventory = add_inventory(data)

        return inventory, 200
