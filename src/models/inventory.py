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

class AttachmentReference(EmbeddedMongoModel):
    attachment = fields.ReferenceField('Attachment')
    filename = fields.CharField(blank=True)

    class Meta:
        connection_alias = 'app'
        final = True

    @staticmethod
    def create(attachment):
        return AttachmentReference(attachment._id, attachment.file.filename)

    def to_json(self):
        return {
            'attachment': str(self.attachment._id),
            'filename': str(self.filename)
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
            attachment_files: [AttachmentReference] List of references to the attachment files
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
    attachment_files = fields.EmbeddedDocumentListField(AttachmentReference, blank=True)

    class Meta:
        connection_alias = 'app'
        final = True

    @staticmethod
    def create(coordinates, inventorydate, method, visibility="", city="", method_info="",
               attachments=False, name="", email="", phone="", more_info="", user=None):
        inventory = Inventory([], inventorydate, method, visibility, city,
                              method_info, attachments, name, email, phone, more_info, user, [])
        inventory.save()

        areas, area_refs = Inventory.create_areas(inventory, coordinates)

        inventory = Inventory.update_areas(inventory, area_refs)

        return [inventory.to_json(hide_personal_info=False), areas]

    @staticmethod
    def create_areas(inventory, coordinates):
        area_refs = []
        areas = []
        for area_coordinates in coordinates:
            new_area = Area.create(inventory, area_coordinates)
            area_refs.append(AreaReference.create(new_area))
            areas.append(new_area.to_json())

        inventory = Inventory.update_areas(inventory, area_refs)

        return areas, area_refs

    @staticmethod
    def update_areas(inventory, new_area_refs):
        inventory.areas = new_area_refs
        return inventory.save()

    @staticmethod
    def update_attachments(inventory, new_attachments):
        inventory.attachment_files = new_attachments
        return inventory.save()

    def to_json(self, hide_personal_info: bool = False):
        # Check if report is made by registered user. Empty email and phone fields if needed
        user_json = None
        if self.user:
            user_json = self.user.to_json()
            if hide_personal_info:
                user_json['email'] = ""
                user_json['phone'] = ""

        # Clear the email and phone number fields if needed
        user_email = "" if hide_personal_info else str(self.email)
        user_phone = "" if hide_personal_info else str(self.phone)

        return {
            'id': str(self._id),
            'areas': [area_ref.to_json() for area_ref in self.areas],
            'user': user_json,
            'inventorydate': str(self.inventorydate)[:-9],
            'method': str(self.method),
            'visibility': str(self.visibility),
            'city': str(self.city),
            'methodInfo': str(self.method_info),
            'attachments': self.attachments,
            'name': str(self.name),
            'email': user_email,
            'phone': user_phone,
            'moreInfo': str(self.more_info),
            'attachment_files': [attach_ref.to_json() for attach_ref in self.attachment_files],
        }
