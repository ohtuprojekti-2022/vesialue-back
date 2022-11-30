from flask import request, send_file
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask_restx import Namespace, Resource
from werkzeug.exceptions import NotFound
from models.attachment import Attachment
from models.inventory import Inventory, AttachmentReference

api = Namespace('files')

@api.route('/upload')
class UploadAttachment(Resource):
    def post(self):
        file = request.files['formFile']
        file.name = file.filename
        att = Attachment(file=file)
        att.save()

        try:
            inventory = Inventory.objects.get(
                {'_id': ObjectId(request.form['inventory'])})
            refs = inventory.attachment_files
            refs.append(AttachmentReference.create(att))
            inventory.attachments_files = refs
            inventory.save()
        except (Inventory.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error


@api.route('/<string:attachment_id>')
class GetAttachment(Resource):
    def get(self, attachment_id):
        # get file from mongodb
        try:
            attachment = Attachment.objects.get(
                {'_id': ObjectId(attachment_id)})
            return send_file(attachment.file, attachment_filename=attachment.file.filename, as_attachment=True)
        except (Attachment.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error