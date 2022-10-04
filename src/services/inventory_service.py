import re
import datetime
from werkzeug.exceptions import BadRequest
from models.inventory import Inventory
from models.area import Area

# COORDINATE_REGEX =
# r'^[NS]([0-8][0-9](\.[0-5]\d){2}|90(\.00){2})\040[EW]((0\d\d|1[0-7]\d)(\.[0-5]\d){2}|180(\.00){2})$'
EMAIL_REGEX = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'


class InventoryService:
    """ Class responsible for inventory logic."""

    def __init__(self):
        """ Class constructor. Creates a new sight service."""

    def add_inventory(self, data):
        all_coordinates = data['coordinates']
        inventorydate = data['inventorydate']
        method = data['method']
        visibility = data["visibility"]
        method_info = data["methodInfo"]
        attachments = data['attachments']
        name = data['name']
        email = data['email']
        phone = data['phone']
        more_info = data['moreInfo']

        self.validate_inventorydate(inventorydate)
        self.validate_method(method)
        self.validate_email(email)

        inventory = Inventory.create(areas=[], inventorydate=inventorydate, method=method,
                                     visibility=visibility, method_info=method_info,
                                     attachments=attachments, name=name, email=email,
                                     phone=phone, more_info=more_info)

        areas = []
        for area_coordinates in all_coordinates:
            areas.append(Area.create(inventory, area_coordinates))

        inventory = Inventory.update_areas(inventory, new_areas=areas)

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
            raise BadRequest(description='Invalid email.')


inventory_service = InventoryService()
