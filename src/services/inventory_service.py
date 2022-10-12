import re
import datetime
from bson.objectid import ObjectId
from bson.errors import InvalidId
from werkzeug.exceptions import BadRequest, NotFound
from models.inventory import Inventory
from models.area import Area
from models.user import User

COORDINATE_REGEX = r"\{'lat': -?[1-9]?[0-9].\d{13,15}, 'lng': -?(1[0-7]?[0-9]|[1-7]?[0-9]|180).\d{13,15}\}"
EMAIL_REGEX = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'


class InventoryService:
    """ Class responsible for inventory logic."""

    def __init__(self):
        """ Class constructor. Creates a new inventory service."""

    def add_inventory(self, data):

        self.validate_missing_parameters(data)
        self.validate_coordinates(data['coordinates'])
        self.validate_inventorydate(data['inventorydate'])
        self.validate_method(data['method'])
        self.validate_email(data['email'])

        user = None
        if data['user']:
            user = User.objects.values().get({'username': data['user']['username']})

        inventory = Inventory.create(areas=[], inventorydate=data['inventorydate'],
                                     method=data['method'], visibility=data['visibility'],
                                     method_info=data['methodInfo'],
                                     attachments=data['attachments'],
                                     name=data['name'], email=data['email'], phone=data['phone'],
                                     more_info=data['moreInfo'], user=user)

        areas = []
        for area_coordinates in data['coordinates']:
            areas.append(Area.create(inventory, area_coordinates))

        inventory = Inventory.update_areas(inventory, new_areas=areas)
        return inventory.to_json()

    def get_inventory(self, inventory_id):
        # pylint: disable=no-member
        inventory = None
        try:
            inventory = Inventory.objects.get({'_id': ObjectId(inventory_id)})
        except (Inventory.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error

        # pylint: enable=no-member
        return inventory.to_json()

    def validate_missing_parameters(self, data):
        properties = [
            'coordinates',
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

    def validate_coordinates(self, coordinates):
        for area in coordinates:
            for point in area:
                if re.fullmatch(COORDINATE_REGEX, str(point)) is None:
                    raise BadRequest(description='Invalid coordinates.')

    def validate_inventorydate(self, inventorydate):
        try:
            datetime.datetime.strptime(inventorydate, '%Y-%m-%d')
        except ValueError as error:
            raise BadRequest(description='Invalid date.') from error

    def validate_method(self, method):
        if method not in ["sight", "echo", "dive", "other"]:
            raise BadRequest(description='Invalid method.')

    def validate_email(self, email):
        if re.fullmatch(EMAIL_REGEX, email) is None:
            raise BadRequest(description='Invalid email.')



inventory_service = InventoryService()
