from flask import request
from flask_restx import Namespace, Resource
from services.user_service import user_service

api = Namespace('user')

@api.route('/admin')
class SetAdmin(Resource):
    """Admin route.
    post:
        summary: Endpoint for setting admin status.
        description: Changes user's admin status to given admin status
        (0 = non-admin, 1 = admin, 2 = super admin).
        responses:
            200:
                description: Returns authentication token
                    and user schema.
            400:
                description: Bad request.
    """
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
    """Route for editing user information.
    put:
        summary: Endpoint for editing user information.
        description: After validation edits user information.
        responses:
            200:
                description: User data has been successfully edited.
                    Returns authentication token and user schema.
            400:
                description: Bad request.
    """
    def put(self):
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {'error': 'bad request'}, 400
        user_data = request.get_json()
        user = user_service.check_authorization(request.headers)
        return user_service.edit(user, user_data), 200

@api.route('/edit-password')
class EditPassword(Resource):
    """Route for changing the password.
    post:
        summary: Endpoint for password change.
        description: Changes password of the user.
        responses:
            200:
                description: Password has been successfully changed.
                    Returns authentication token and user schema.
            400: Bad request.
    """
    def post(self):
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {'error': 'bad request'}, 400
        data = request.get_json()
        user = user_service.check_authorization(request.headers)
        return user_service.edit_password(user, data['current_password'], data['new_password']), 200
