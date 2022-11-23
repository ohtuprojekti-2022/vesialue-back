from flask import request
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask_restx import Namespace, Resource
from werkzeug.exceptions import NotFound
from models.attachment import Attachment
from models.inventory import Inventory

api = Namespace('upload')

@api.route('')
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