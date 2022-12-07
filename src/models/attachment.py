from pymodm import MongoModel, fields

class Attachment(MongoModel):
    class Meta:
        connection_alias = 'app'
        final = True

    _id = fields.ObjectId()
    file = fields.FileField(required=True)
