from pymodm import MongoModel, fields

class Attachment(MongoModel):
    _id = fields.ObjectId()
    file = fields.FileField(required=True)