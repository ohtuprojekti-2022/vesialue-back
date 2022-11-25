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
        is_admin = user_service.check_admin(request.headers)
        inventory = inventory_service.add_inventory(data, user, is_admin)

        return inventory, 201

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

        return inventory, 201

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
    
    def delete(self, report_id):
        is_admin = user_service.check_admin(request.headers)
        inventory_service.delete_inventory(report_id, is_admin)
        return 200

    def put(self, report_id):
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {'error': 'bad request'}, 400
        data = request.get_json()

        is_admin = user_service.check_admin(request.headers)

        inventory = inventory_service.approve_edit(report_id, is_admin)

        return inventory, 200


@api.route('/areas')
class GetAreas(Resource):
    def get(self):
        return inventory_service.get_areas(), 200

@api.route('/delete')
class DeleteRequest(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {'error': 'bad request'}, 400

        data = request.get_json()
        user = user_service.check_authorization(request.headers)
        deletion = inventory_service.request_deletion(data, user)
        return deletion, 201
    
    def get(self):
        is_admin = user_service.check_admin(request.headers)
        return user_service.get_all_delete_requests(is_admin), 200

@api.route('/delete/<string:del_request_id>')
class HandleDeleteRequest(Resource):
    def delete(self, del_request_id):
        is_admin = user_service.check_admin(request.headers)
        inventory_service.remove_delete_request(del_request_id, is_admin)
        return 200

    def put(self, del_request_id):
        is_admin = user_service.check_admin(request.headers)
        inventory_service.approve_deletion(del_request_id, is_admin)
        return 200
