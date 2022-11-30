from pymodm import MongoModel, fields, ReferenceField
from models.inventory import Inventory
from models.user import User
from bson.objectid import ObjectId

class DeleteRequest(MongoModel):
    _id = fields.ObjectId()
    user = ReferenceField(User, blank=False)
    inventory = ReferenceField(Inventory, on_delete=ReferenceField.CASCADE)
    reason = fields.CharField(blank=False)
    
    class Meta:
        '''Defines MongoDB options for this model'''
        connection_alias = 'app'
        final = True
    
    @staticmethod
    def create(user, inventory_id, reason):
        inventory = Inventory.objects.values().get({'_id': ObjectId(inventory_id)})
        delete_request = DeleteRequest(user, inventory, reason)
        delete_request.save()
        return delete_request

    def to_json(self):
        return {'id': str(self._id),
             'user': self.user.to_json(),
             'inventory': str(self.inventory._id),
             'reason': str(self.reason)
        }