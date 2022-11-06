from pymodm import EmbeddedMongoModel, MongoModel, fields, ReferenceField
from models.inventory import Inventory
from models.user import User
from bson.objectid import ObjectId

class Point(EmbeddedMongoModel):
    lat = fields.FloatField(required=True)
    lng = fields.FloatField(required=True)

    class Meta:
        connection_alias = 'app'
        final = True

    @staticmethod
    def create(lat_lng):
        return Point(lat_lng['lat'], lat_lng['lng'])

    def to_json(self):
        return {
            'lat': self.lat,
            'lng': self.lng
        }


class EditedArea(EmbeddedMongoModel):
    coordinates = fields.EmbeddedDocumentListField(Point)

    class Meta:
        connection_alias = 'app'
        final = True

    @staticmethod
    def create(coordinates):
        coordinate_points = []
        for lat_lng in coordinates:
            coordinate_points.append(Point.create(lat_lng))
        area = EditedArea(coordinates=coordinate_points)
        return area

    def to_json(self):
        coordinates = []
        for point in self.coordinates:
            coordinates.append(point.to_json())
        return {
            'coordinates': coordinates
        }




class EditedInventory(MongoModel):
    """ Class that represents a single edited inventory.
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
            original_report: [INVENTORY] the original inventory report
    """

    _id = fields.ObjectId()
    areas = fields.EmbeddedDocumentListField(EditedArea, blank=True)
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
    original_report = ReferenceField(Inventory)

    class Meta:
        connection_alias = 'app'
        final = True

    @staticmethod
    def create(coordinates, inventorydate, method, visibility="", method_info="",
               attachments=False, name="", email="", phone="", more_info="",
               user=None, original_report=None):
        report_obj = Inventory.objects.values().get({'_id': ObjectId(original_report)})
        inventory = EditedInventory([], inventorydate, method, visibility,
                              method_info, attachments, name, email, phone, more_info, user, report_obj)
        inventory.save()


        areas = []
        for area_coordinates in coordinates:
            new_area = EditedArea.create(area_coordinates)
            areas.append(new_area.to_json())

        inventory = EditedInventory.update_areas(inventory, areas)

        return inventory.to_json()

    @staticmethod
    def update_areas(inventory, new_area_refs):
        inventory.areas = new_area_refs
        return inventory.save()

    def to_json(self):
        area_refs = []
        for area_ref in self.areas:
            area_refs.append(area_ref.to_json())
        user_json = None
        if self.user:
            user_json = self.user.to_json()
        return {
            'id': str(self._id),
            'areas': area_refs,
            'user': user_json,
            'inventorydate': str(self.inventorydate)[:-9],
            'method': str(self.method),
            'visibility': str(self.visibility),
            'methodInfo': str(self.method_info),
            'attachments': self.attachments,
            'name': str(self.name),
            'email': str(self.email),
            'phone': str(self.phone),
            'moreInfo': str(self.more_info),
            'originalReport': str(self.original_report._id)
        }
