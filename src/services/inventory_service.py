import re
import datetime
from werkzeug.exceptions import BadRequest
from models.inventory import Inventory

COORDINATE_REGEX = r'^[NS]([0-8][0-9](\.[0-5]\d){2}|90(\.00){2})\040[EW]((0\d\d|1[0-7]\d)(\.[0-5]\d){2}|180(\.00){2})$'
EMAIL_REGEX = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'

class InventoryService:
    """ Class responsible for inventory logic."""

    def __init__(self):
        """ Class constructor. Creates a new sight service."""

    def add_inventory(self, data):
        properties = [
            'coordinates',
            'inventorydate',
            'method',
            'attachments',
            'name',
            'email',
            'phone',
            'more_info'
        ]

        for key in properties:
            if not key in data:
                raise BadRequest(description='invalid request, missing '+key)

        self.validate_inventorydate(data['inventorydate'])
        self.validate_method(data['method'])
        self.validate_email(data['email'])

        inventory = Inventory.create(data['coordinates'], data['inventorydate'], data['method'],
            		  data['attachments'], data['name'], data['email'], data['phone'], data['more_info'])

        return inventory.to_json()

    def validate_inventorydate(self, inventorydate):
        try:
            datetime.datetime.strptime(inventorydate, '%Y-%m-%d')
        except ValueError:
            raise BadRequest(description='Invalid date.')

    def validate_method(self, method):
        if method not in ["sight", "echo", "dive", "other"]:
            raise BadRequest(description='Invalid method.')

    def validate_email(self, email):
        if re.fullmatch(EMAIL_REGEX, email) is None:
            print('jee')
            raise BadRequest(description='Invalid email.')

inventory_service = InventoryService()
