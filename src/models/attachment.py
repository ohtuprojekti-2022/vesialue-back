from pymodm import MongoModel, fields
from .inventory import Inventory

class Attachment(MongoModel):
    class Meta:
        connection_alias = 'app'
        final = True

    _id = fields.ObjectId()
    file = fields.FileField(required=True)
    inventory = fields.ReferenceField(Inventory, required=True)
