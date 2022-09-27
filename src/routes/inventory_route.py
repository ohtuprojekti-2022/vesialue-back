from argparse import Namespace
from flask import request
from flask_restx import Namespace, Resource
from models.inventory import Inventory

api = Namespace('add_inventory')

@api.route('/')
class AddInventory(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {'error': 'bad request'}, 400
        data = request.get_json()

        coordinates = data['coordinates']
        time = data['time']
        methods = data['methods']
        attachments = data['attachments']
        name = data['name']
        email = data['email']
        phonenumber = data['phonenumber']
        other = data['other']

        Inventory.create(coordinates=coordinates, time=time, methods=methods,
        		  attachments=attachments, name=name, email=email, phonenumber=phonenumber, other=other)
        return {'message': 'success'}, 200

