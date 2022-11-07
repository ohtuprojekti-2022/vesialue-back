import requests
from bson.objectid import ObjectId
from bson.errors import InvalidId
from werkzeug.exceptions import BadRequest, NotFound
from utils.config import BIG_DATA_API_KEY
from models.inventory import Inventory
from models.edited_inventory import EditedInventory
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
        validation.validate_coordinates(data['areas'])
        validation.validate_inventorydate_date(data['inventorydate'])
        validation.validate_method(data['method'])
        if user is None:
            validation.validate_email(data['email'])
            validation.validate_phone(data['phone'])
        else:
            validation.validate_email(user.email)
            validation.validate_phone(user.phone)
        self.validate_original_inventory_id(data['originalReport'])

        inventory = EditedInventory.create(data['areas'], inventorydate=data['inventorydate'],
                                     method=data['method'], visibility=data['visibility'],
                                     method_info=data['methodInfo'],
                                     attachments=data['attachments'],
                                     name=data['name'], email=data['email'], phone=data['phone'],
                                     more_info=data['moreInfo'], user=user, original_report=data['originalReport'])

        return inventory

    def get_inventory(self, inventory_id):
        inventory = None
        try:
            inventory = Inventory.objects.get({'_id': ObjectId(inventory_id)})
        except (Inventory.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error

        return inventory.to_json()

    def get_edited_inventory(self, inventory_id):
        inventory = None
        try:
            inventory = EditedInventory.objects.get({'_id': ObjectId(inventory_id)})
        except (EditedInventory.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error

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
