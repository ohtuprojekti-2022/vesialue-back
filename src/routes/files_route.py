from flask import request, send_file
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask_restx import Namespace, Resource
from werkzeug.exceptions import NotFound
from models.attachment import Attachment
from models.inventory import Inventory

api = Namespace('files')

@api.route('/upload')
class UploadAttachment(Resource):
    def post(self):
        print(request.form)
        file = request.files['formFile']
        print(file)
        try:
            inventory = Inventory.objects.get(
                {'_id': ObjectId(request.form['inventory'])})
        except (Inventory.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error

        att = Attachment(file=file.read(), inventory=inventory)
        att.save()

@api.route('/<string:attachment_id>')
class GetAttachment(Resource):
    def get(self, attachment_id):
        print(attachment_id)
        # get file from mongodb
        try:
            attachment = Attachment.objects.get(
                {'_id': ObjectId(attachment_id)})
            return send_file(attachment.file, attachment_filename="test.png")
        except (Attachment.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error
