from flask import request
from flask_restx import Namespace, Resource
from services.inventory_service import inventory_service
from services.user_service import user_service


api = Namespace('inventory')


@api.route('')
class AddInventory(Resource):
    """Route for all inventories.
    post:
        summary: Endpoint for creating a new inventory.
        description: Creates a new inventory and returns all
            inventories.
        responses:
            201:
                description: Inventory has been successfully added.
            400:
                description: Bad request.
    get:
        summary: Endpoint for getting all inventories.
        description: Returns all inventories. Certain fields
            may be hidden if the user is not an admin.
        responses:
            200:
                description: Inventories have been returned
                    successfully.
    """
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
    """Route for all edited inventories.
    post:
        summary: Endpoint for making a new edit request.
        description: Creates a new edited inventory. Any older edit requests 
            made for the same inventory will be deleted.
        responses:
            201:
                description: A new edit request was successfully made.
            400:
                description: Bad request.
            401:
                description: Unauthorized.
    get:
        summary: Endpoint for getting all edited inventories.
        description: Returns all edited inventories if the user is
            an admin.
        responses:
            200:
                description: Returns all edited inventories.
            400:
                description: Bad request.
            401:
                description: Unauthorized.
    """
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
        if not is_admin:
            user = user_service.check_authorization(request.headers)
            if user:
                return inventory_service.get_edited_inventories_by_user_id(user._id)
            else:
                return {'error': 'bad request'}, 400
        return inventory_service.get_all_edited_inventories(is_admin), 200


@api.route('/edit/<string:report_id>')
class GetEdited(Resource):
    """Route for individual edited inventories.
    get:
        summary: Endpoint for getting an edited inventory.
        description: Returns an individual edited inventory according
            to ID, if the user is an admin.
        parameters:
            - name: report_id
                in: path
                description: ID of the edited inventory.
                type: string
                required: true
        responses:
            200:
                description: Returns edited inventory schema.
            401:
                description: Unauthorized.
            404:
                description: Edited inventory not found.
    delete:
        summary: Endpoint for deleting an edited inventory.
        description: Deletes an individual edited inventory
            if the user is an admin.
        parameters:
            - name: report_id
                in: path
                description: ID of the edited inventory.
                type: string
                required: true
        responses:
            200:
                description: Given edited inventory is deleted.
            401:
                description: Unauthorized.
            404:
                description: Edited inventory not found.
    """
    def get(self, report_id):
        is_admin = user_service.check_admin(request.headers)
        inventory = inventory_service.get_edited_inventory(report_id, is_admin)
        return inventory, 200

    def delete(self, report_id):
        is_admin = user_service.check_admin(request.headers)
        user = user_service.check_authorization(request.headers)
        inventory_service.delete_edit(report_id, is_admin, user._id)
        return 200


@api.route('/<string:report_id>')
class GetInventory(Resource):
    """Route for individual inventories.
    get:
        summary: Endpoint for getting an inventory.
        description: Returns an individual inventory according
            to ID.
        parameters:
            - name: report_id
                in: path
                description: ID of the inventory.
                type: string
                required: true
        responses:
            200:
                description: Returns inventory schema.
            404:
                description: Inventory not found.
    delete:
        summary: Endpoint for deleting an inventory.
        description: Deletes an individual inventory
            if the user is an admin.
        parameters:
            - name: report_id
                in: path
                description: ID of the inventory.
                type: string
                required: true
        responses:
            200:
                description: Given inventory is deleted.
            401:
                description: Unauthorized.
            404:
                description: Inventory not found.
    put:
        summary: Endpoint for editing an inventory.
        description: Edits the data of the given inventory
            using data received from the frontend, if the
            user is an admin.
        parameters:
            - name: report_id
                in: path
                description: ID of the inventory.
                type: string
                required: true
        responses:
            200:
                description: Given inventory is edited.
            401:
                description: Unauthorized.
            404:
                description: Inventory not found.
    """
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

        is_admin = user_service.check_admin(request.headers)

        inventory = inventory_service.approve_edit(report_id, is_admin)

        return inventory, 200


@api.route('/areas')
class GetAreas(Resource):
    """Route for all areas.
    get:
        summary: Endpoint for getting all areas.
        description: Returns all areas.
        responses:
            200:
                description: Returns all areas.
    """
    def get(self):
        return inventory_service.get_areas(), 200


@api.route('/delete')
class DeleteRequest(Resource):
    """Route for all delete requests.
    post:
        summary: Endpoint for making a new delete request.
        description:
        responses:
            201:
                description: A new delete request has been successfully
                    made.
            400:
                description: Bad request.
    get:
        summary: Endpoint for getting all delete requests.
        description: Returns delete requests according to admin status.
        responses:
            200:
                description: Returns all delete requests if user is admin,
                    otherwise only the user's own delete requests are returned.
            400:
                description: Bad request.
    """
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
        if not is_admin:
            user = user_service.check_authorization(request.headers)
            if user:
                return inventory_service.get_delete_requests_by_user_id(user._id)
            else:
                return {'error': 'bad request'}, 400
        return inventory_service.get_all_delete_requests(is_admin), 200


@api.route('/delete/<string:del_request_id>')
class HandleDeleteRequest(Resource):
    """Route for individual delete requests.
    delete:
        summary: Endpoint for deleting a delete request.
        description: Deletes a delete request if user is an admin.
        parameters:
            - name: request_id
                in: path
                description: ID of the delete request.
                type: string
                required: true
        responses:
            200:
                description: Delete request has been deleted.
            401:
                description: Unauthorized.
            404:
                description: Delete request not found.
    put:
        summary: Endpoint for approving a delete request.
        description: Deletes a delete request and the inventory
            that was requested to be deleted if the user is an admin.
        parameters:
            - name: request_id
                in: path
                description: ID of the delete request.
                type: string
                required: true
        responses:
            200:
                description: The delete request has been approved. The inventory and
                    the delete request have been removed.
            401:
                description: Unauthorized.
            404:
                description: Delete request not found.
    """
    def delete(self, del_request_id):
        is_admin = user_service.check_admin(request.headers)
        user = user_service.check_authorization(request.headers)
        inventory_service.remove_delete_request(del_request_id, is_admin, user._id)
        return 200

    def put(self, del_request_id):
        is_admin = user_service.check_admin(request.headers)
        inventory_service.approve_deletion(del_request_id, is_admin)
        return 200
