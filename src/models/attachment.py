from pymodm import MongoModel, fields
from .inventory import Inventory

class Attachment(MongoModel):
    """Class that represents an attachment file.
    Attributes:
        file: [File] Attached file.
        inventory: [INVENTORY] Inventory the attachment is attached to.
    """
    class Meta:
        connection_alias = 'app'
        final = True

    _id = fields.ObjectId()
    file = fields.FileField(required=True)
    inventory = fields.ReferenceField(Inventory, required=True)
