import os
from flask import request, send_file
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask_restx import Namespace, Resource
from werkzeug.exceptions import NotFound, BadRequest
from models.attachment import Attachment
from models.inventory import Inventory, AttachmentReference
from models.user import User
from services.user_service import user_service

# Disable pylint's no-member check since it causes unnecessary warnings when used with pymodm
# pylint: disable=no-member

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
            attachment = Attachment(file=file, inventory=inventory)
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
        # Get the attachment object from mongo
        try:
            attachment = Attachment.objects.get(
                {'_id': ObjectId(attachment_id)}
            )
        except (Attachment.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error
        print(attachment)

        # Get the inventory associated with the attachment
        try:
            inventory = Inventory.objects.get(
                {'_id': ObjectId(attachment.inventory._id)}
            )
        except (Inventory.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error
        print(inventory)

        # Get user from the token
        user = user_service.check_authorization(request.headers)
        if not user:
            return {'error': 'bad request'}, 400
        
        # Check if user matches the inventory's user
        if str(user._id) == str(inventory.user._id):
            # Delete the attachment, included file data and reference from the report
            try:
                references = inventory.attachment_files
                # Delete reference from the inventory
                for ref in references:
                    if str(ref.attachment._id) == str(attachment_id):
                        references.remove(ref)
                inventory.attachment_files = references
                inventory.save()

                # Delete file data
                attachment.file.delete()

                # Delete attachment object
                Attachment.objects.raw({'_id': ObjectId(attachment_id)}).delete()
            except (Attachment.DoesNotExist, InvalidId) as error:
                raise NotFound(description='404 not found') from error
        else:
            return {'error': 'bad request'}, 400

        return {'deleted': attachment_id}, 204
# pylint: enable=no-member
