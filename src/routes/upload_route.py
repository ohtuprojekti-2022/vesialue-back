from flask import request
from flask_restx import Namespace, Resource
from models.attachment import Attachment

api = Namespace('upload')

@api.route('')
class UploadAttachment(Resource):
    def post(self):
        print(request.files)
        file = request.files['formFile']
        print(file)
        att = Attachment(file=file.read())
        att.save()