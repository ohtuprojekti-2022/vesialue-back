import re
import datetime
import requests
from bson.objectid import ObjectId
from bson.errors import InvalidId
from werkzeug.exceptions import BadRequest, NotFound
from utils.config import BIG_DATA_API_KEY
from models.inventory import Inventory
from models.edited_inventory import EditedInventory
from models.area import Area

COORDINATE_REGEX = r"\{'lat': -?[1-9]?[0-9].\d{10,15}, 'lng': -?(1[0-7]?[0-9]|[1-7]?[0-9]|180).\d{10,15}\}"
EMAIL_REGEX = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
PHONE_REGEX = r'^((04[0-9]{1})(\s?|-?)|050(\s?|-?)|0457(\s?|-?)|[+]?358(\s?|-?)50|0358(\s?|-?)50|00358(\s?|-?)50|[+]?358(\s?|-?)4[0-9]{1}|0358(\s?|-?)4[0-9]{1}|00358(\s?|-?)4[0-9]{1})(\s?|-?)(([0-9]{3,4})(\s|\-)?[0-9]{1,4})$'


class InventoryService:
    """ Class responsible for inventory logic."""

    def __init__(self):
        """ Class constructor. Creates a new inventory service."""

    def add_inventory(self, data, user):

        self.validate_missing_parameters(data)
        self.validate_coordinates(data['areas'])
        self.validate_inventorydate_format(data['inventorydate'])
        self.validate_inventorydate_date(data['inventorydate'])
        self.validate_method(data['method'])
        self.validate_method_info(data['method'], data['methodInfo'])
        self.validate_more_info(data['moreInfo'])
        self.validate_email(
            data['email']) if user is None else self.validate_email(user.email)
        self.validate_phone(
            data['phone']) if user is None else self.validate_phone(user.phone)

        city = self.get_city(self.get_center(data['areas']))

        inventory = Inventory.create(data['areas'], inventorydate=data['inventorydate'],
                                     method=data['method'], visibility=data['visibility'],
                                     city=city,
                                     method_info=data['methodInfo'],
                                     attachments=data['attachments'],
                                     name=data['name'], email=data['email'], phone=data['phone'],
                                     more_info=data['moreInfo'], user=user)
        return inventory

    def add_edited_inventory(self, data, user):
        self.validate_missing_parameters(data)
        self.validate_coordinates(data['areas'])
        self.validate_inventorydate_date(data['inventorydate'])
        self.validate_method(data['method'])
        self.validate_email(
            data['email']) if user is None else self.validate_email(user.email)
        self.validate_phone(
            data['phone']) if user is None else self.validate_phone(user.phone)
        self.validate_original_inventory_id(data['originalReport'])
        
        inventory = EditedInventory.create(data['areas'], inventorydate=data['inventorydate'],
                                     method=data['method'], visibility=data['visibility'],
                                     method_info=data['methodInfo'],
                                     attachments=data['attachments'],
                                     name=data['name'], email=data['email'], phone=data['phone'],
                                     more_info=data['moreInfo'], user=user, original_report=data['originalReport'])
        return inventory

    def get_inventory(self, inventory_id):
        # pylint: disable=no-member
        inventory = None
        try:
            inventory = Inventory.objects.get({'_id': ObjectId(inventory_id)})
        except (Inventory.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error

        # pylint: enable=no-member
        return inventory.to_json()

    def get_edited_inventory(self, inventory_id):
        # pylint: disable=no-member
        inventory = None
        try:
            inventory = EditedInventory.objects.get({'_id': ObjectId(inventory_id)})
        except (EditedInventory.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error

        # pylint: enable=no-member
        return inventory.to_json()

    def validate_original_inventory_id(self, id):
        try:
            self.get_inventory(id)
        except:
            raise BadRequest(description='Invalid original report id.')

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

    def validate_coordinates(self, coordinates):
        for area in coordinates:
            for point in area:
                if re.fullmatch(COORDINATE_REGEX, str(point)) is None:
                    raise BadRequest(description='Invalid areas.')

    def validate_inventorydate_format(self, inventorydate):
        try:
            datetime.datetime.strptime(inventorydate, '%Y-%m-%d')
        except ValueError as error:
            raise BadRequest(description='Invalid date.') from error

    def validate_inventorydate_date(self, inventorydate):
        if datetime.datetime.strptime(inventorydate, '%Y-%m-%d') > datetime.datetime.today():
            raise BadRequest(description='Date cannot be in the future.')

    def validate_method(self, method):
        if method not in ["sight", "echo", "dive", "other"]:
            raise BadRequest(description='Invalid method.')

    def validate_email(self, email):
        if re.fullmatch(EMAIL_REGEX, email) is None:
            raise BadRequest(description='Invalid email.')

    def validate_phone(self, phone):
        if phone == '':
            pass
        elif re.fullmatch(PHONE_REGEX, phone) is None:
            raise BadRequest(description='Invalid phone number.')

    def validate_method_info(self, method, method_info):
        if method == 'other':
            if len(method_info) > 100:
                raise BadRequest(description='Method info too long.')
            elif method_info == "":
                raise BadRequest(description='No method info given.')

    def validate_more_info(self, more_info):
        if len(more_info) > 500:
            raise BadRequest(description='Info too long.')

    def get_center(self, coordinates):
        max_lat = -90.0
        min_lat = 90.0
        max_lng = -180.0
        min_lng = 180.0

        for area in coordinates:
            for point in area:
                max_lat = max(point['lat'], max_lat)
                min_lat = min(point['lat'], min_lat)
                max_lng = max(point['lng'], max_lng)
                min_lng = min(point['lng'], min_lng)

        return ((max_lat + min_lat) / 2), ((max_lng + min_lng) / 2)

    def get_city(self, center):
        params = dict(
            latitude=center[0],
            longitude=center[1],
            localityLanguage='fi',
            key=BIG_DATA_API_KEY
        )

        url = 'https://api.bigdatacloud.net/data/reverse-geocode'
        response = requests.get(url=url, params=params).json()
        if not response['city'] or not response['locality']:
            return "Unknown location"
        if response['city'] != "":
            return f"{response['city']}, {response['locality']}"
        else:
            return response['locality']

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

    def get_all_edited_inventories(self):
        inventories = []
        for item in EditedInventory.objects.all():
            inventories.append(item.to_json())

        return inventories

inventory_service = InventoryService()
