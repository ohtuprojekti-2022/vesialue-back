from pymodm import MongoModel, fields, ReferenceField
from models.area import Area
from models.user import User


class Inventory(MongoModel):
    """ Class that represents a single inventory.
        Attributes:
            areas: [String] areas of the inventory area.
            user: [USER] user that submitted the inventory.
            inventorydate: [String] Time of the inventory.
            method: [String] sight || echo || dive || other
            visibility: [String] bad || normal || good
            method_info: [String] Description of method if method == other
            attachments: [boolean] True if there are attachments included.
            name: [String] The name of the submitter.
            email: [String] The email of the submitter.
            phone: [String] The phonenumber of the submitter.
            more_info: [String] Other notes for the inventory.
    """

    _id = fields.ObjectId()
    areas = fields.EmbeddedDocumentListField(Area, blank=True)
    inventorydate = fields.DateTimeField(required=True)
    method = fields.CharField(required=True)
    visibility = fields.CharField(blank=True)
    method_info = fields.CharField(blank=True)
    attachments = fields.BooleanField(required=True, default=False)
    name = fields.CharField(blank=True)
    email = fields.CharField(blank=True)
    phone = fields.CharField(blank=True)
    more_info = fields.CharField(blank=True)
    user = ReferenceField(User, blank= True)

    class Meta:
        connection_alias = 'app'
        final = True

    @staticmethod
    def create(areas, inventorydate, method, visibility="", method_info="",
               attachments=False, name="", email="", phone="", more_info="", user=None):
        inventory = Inventory(areas, inventorydate, method, visibility,
                              method_info, attachments, name, email, phone, more_info, user)
        inventory.save()
        return inventory

    @staticmethod
    def update_areas(inventory, new_areas):
        inventory.areas = new_areas
        return inventory.save()

    def to_json(self):
        areas = []
        for area in self.areas:
            areas.append(area.to_json(simple=True))
        user_json = None
        if self.user:
        	user_json = self.user.to_json()
        return {
            'id': str(self._id),
            'areas': areas,
            'user': user_json,
            'inventorydate': str(self.inventorydate),
            'method': str(self.method),
            'attachments': self.attachments,
            'name': str(self.name),
            'email': str(self.email),
            'phone': str(self.phone),
            'moreInfo': str(self.more_info)
        }
