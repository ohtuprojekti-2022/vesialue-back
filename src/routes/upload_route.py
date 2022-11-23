from flask import request
from flask_restx import Namespace, Resource

api = Namespace('upload')

@api.route('')
class UploadAttachment(Resource):
    def post(self):
        print(request.files)
        file = request.files['formFile']
        print(file)