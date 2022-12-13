from flask import request, send_file
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask_restx import Namespace, Resource
from werkzeug.exceptions import NotFound
from models.attachment import Attachment
from services.user_service import user_service
from services.inventory_service import inventory_service

# Disable pylint's no-member check since it causes unnecessary warnings when used with pymodm
# pylint: disable=no-member

api = Namespace('files')

@api.route('/upload')
class UploadAttachment(Resource):
    def post(self):
        return inventory_service.add_attachment(
            inventory_id=request.form['inventory'],
            attachment_files=request.files.getlist("file")
        )

@api.route('/<string:attachment_id>')
class GetAttachment(Resource):
    def get(self, attachment_id):
        # Get file from mongodb
        try:
            attachment = Attachment.objects.get(
                {'_id': ObjectId(attachment_id)})
            return send_file(
                attachment.file,
                attachment_filename=attachment.file.filename,
                as_attachment=True)
        except (Attachment.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error

    def delete(self, attachment_id):
        # Get user from the token
        user = user_service.check_authorization(request.headers)
        if not user:
            return {'error': 'bad request'}, 400

        return inventory_service.delete_attachment(
            attachment_id,
            user,
            user_service.check_admin(request.headers)
        )

# pylint: enable=no-member
