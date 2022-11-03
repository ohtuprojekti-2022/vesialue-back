from bson.objectid import ObjectId
from bson.errors import InvalidId
from werkzeug.exceptions import BadRequest, NotFound
from models.inventory import Inventory
from models.area import Area
from services.validation import validation

class InventoryService:
    """ Class responsible for inventory logic."""

    def __init__(self):
        """ Class constructor. Creates a new inventory service."""

    def add_inventory(self, data, user):

        self.validate_missing_parameters(data)
        validation.validate_coordinates(data['areas'])
        validation.validate_inventorydate_format(data['inventorydate'])
        validation.validate_inventorydate_date(data['inventorydate'])
        validation.validate_method(data['method'])
        validation.validate_method_info(data['method'], data['methodInfo'])
        validation.validate_more_info(data['moreInfo'])
        if user is None:
            validation.validate_email(data['email'])
            validation.validate_phone(data['phone'])
        else:
            validation.validate_email(user.email)
            validation.validate_phone(user.phone)

        inventory = Inventory.create(data['areas'], inventorydate=data['inventorydate'],
                                     method=data['method'], visibility=data['visibility'],
                                     method_info=data['methodInfo'],
                                     attachments=data['attachments'],
                                     name=data['name'], email=data['email'], phone=data['phone'],
                                     more_info=data['moreInfo'], user=user)

        return inventory

    def get_inventory(self, inventory_id):
        inventory = None
        try:
            inventory = Inventory.objects.get({'_id': ObjectId(inventory_id)})
        except (Inventory.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error

        return inventory.to_json()

    def validate_missing_parameters(self, data):
        properties = [
            'areas',
            'inventorydate',
            'method',
            'visibility',
            'methodInfo',
            'attachments',
            'name',
            'email',
            'phone',
            'moreInfo'
        ]

        for key in properties:
            if not key in data:
                raise BadRequest(description='Invalid request, missing '+key)

    def get_areas(self):
        areas = []
        for area in Area.objects.all():
            areas.append(area.to_json())

        return areas

    def get_all_inventories(self):
        inventories = []
        for item in Inventory.objects.all():
            inventories.append(item.to_json())

        return inventories

inventory_service = InventoryService()
