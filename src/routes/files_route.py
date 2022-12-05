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
        # Get the inventory, return 404 if not found
        try:
            inventory = Inventory.objects.get(
                {'_id': ObjectId(request.form['inventory'])})
        except (Inventory.DoesNotExist, InvalidId) as error:
            raise NotFound(description='invalid inventory') from error

        # Get attachments from the form
        attachments = []
        for file in request.files.getlist("file"):
            file.name = file.filename
            attachment = Attachment(file=file)
            attachment.save()
            attachments.append(attachment)

        # Append references of the files to the inventory
        references = inventory.attachment_files
        for attachment in attachments:
            references.append(AttachmentReference.create(attachment))
        inventory.attachment_files = references
        inventory.save()

        # Return attachment files as json
        return [reference.to_json() for reference in references]

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
