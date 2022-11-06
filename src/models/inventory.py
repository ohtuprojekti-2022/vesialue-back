from pymodm import EmbeddedMongoModel, MongoModel, fields, ReferenceField
from models.area import Area
from models.user import User


class AreaReference(EmbeddedMongoModel):
    area = fields.ReferenceField('Area')

    class Meta:
        connection_alias = 'app'
        final = True

    @staticmethod
    def create(area):
        return AreaReference(area._id)

    def to_json(self):
        return {
            'area': str(self.area._id)
        }


class Inventory(MongoModel):
    """ Class that represents a single inventory.
        Attributes:
            areas: [String] areas of the inventory area.
            user: [USER] user that submitted the inventory.
            inventorydate: [String] Time of the inventory.
            method: [String] sight || echo || dive || other
            visibility: [String] bad || normal || good
            city: [String] Name of city or region.
            method_info: [String] Description of method if method == other
            attachments: [boolean] True if there are attachments included.
            name: [String] The name of the submitter.
            email: [String] The email of the submitter.
            phone: [String] The phonenumber of the submitter.
            more_info: [String] Other notes for the inventory.
    """

    _id = fields.ObjectId()
    areas = fields.EmbeddedDocumentListField(AreaReference, blank=True)
    inventorydate = fields.DateTimeField(required=True)
    method = fields.CharField(required=True)
    visibility = fields.CharField(blank=True)
    city = fields.CharField(blank=True)
    method_info = fields.CharField(blank=True)
    attachments = fields.BooleanField(required=True, default=False)
    name = fields.CharField(blank=True)
    email = fields.CharField(blank=True)
    phone = fields.CharField(blank=True)
    more_info = fields.CharField(blank=True)
    user = ReferenceField(User, blank=True)

    class Meta:
        connection_alias = 'app'
        final = True

    @staticmethod
    def create(coordinates, inventorydate, method, visibility="", city="", method_info="",
               attachments=False, name="", email="", phone="", more_info="", user=None):
        inventory = Inventory([], inventorydate, method, visibility, city,
                              method_info, attachments, name, email, phone, more_info, user)
        inventory.save()

        area_refs = []
        areas = []
        for area_coordinates in coordinates:
            new_area = Area.create(inventory, area_coordinates)
            area_refs.append(AreaReference.create(new_area))
            areas.append(new_area.to_json())

        inventory = Inventory.update_areas(inventory, area_refs)

        return [inventory.to_json(hide_email=False), areas]

    @staticmethod
    def update_areas(inventory, new_area_refs):
        inventory.areas = new_area_refs
        return inventory.save()

    def to_json(self, hide_email: bool = False):
        area_refs = []
        for area_ref in self.areas:
            area_refs.append(area_ref.to_json())

        # Check if report is made by registered user. Empty email field if needed
        user_json = None
        if self.user:
            user_json = self.user.to_json()
            if hide_email:
                user_json['email'] = ""

        # Clear the email field if needed
        user_email = "" if hide_email else str(self.email)

        return {
            'id': str(self._id),
            'areas': area_refs,
            'user': user_json,
            'inventorydate': str(self.inventorydate)[:-9],
            'method': str(self.method),
            'visibility': str(self.visibility),
            'city': str(self.city),
            'methodInfo': str(self.method_info),
            'attachments': self.attachments,
            'name': str(self.name),
            'email': user_email,
            'phone': str(self.phone),
            'moreInfo': str(self.more_info)
        }
