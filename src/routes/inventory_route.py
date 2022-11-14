from flask import request
from flask_restx import Namespace, Resource
from services.inventory_service import inventory_service
from services.user_service import user_service


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

    def put(self):
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {'error': 'bad request'}, 400
        data = request.get_json()

        is_admin = user_service.check_admin(request.headers)
        
        inventory = inventory_service.approve_edit(data['id'], is_admin)

        return inventory, 200

    def get(self):
        is_admin = user_service.check_admin(request.headers)
        return inventory_service.get_all_inventories(is_admin), 200

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
        is_admin = user_service.check_admin(request.headers)
        return inventory_service.get_all_edited_inventories(is_admin), 200

@api.route('/edit/<string:report_id>')
class GetEdited(Resource):
    def get(self, report_id):
        is_admin = user_service.check_admin(request.headers)
        inventory = inventory_service.get_edited_inventory(report_id, is_admin)
        return inventory, 200

    def delete(self, report_id):
        is_admin = user_service.check_admin(request.headers)
        inventory_service.delete_edit(report_id, is_admin)
        return 200

@api.route('/<string:report_id>')
class GetInventory(Resource):
    def get(self, report_id):
        is_admin = user_service.check_admin(request.headers)
        inventory = inventory_service.get_inventory(report_id, is_admin)
        return inventory, 200

@api.route('/areas')
class GetAreas(Resource):
    def get(self):
        return inventory_service.get_areas(), 200
