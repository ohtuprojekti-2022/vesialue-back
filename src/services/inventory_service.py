import re
import datetime
from bson.objectid import ObjectId
from bson.errors import InvalidId
from werkzeug.exceptions import BadRequest, NotFound
from models.inventory import Inventory
from models.edited_inventory import EditedInventory
from models.area import Area
from models.user import User
from copy import copy

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
        self.validate_inventorydate(data['inventorydate'])
        self.validate_method(data['method'])
        self.validate_email(
            data['email']) if user is None else self.validate_email(user.email)
        self.validate_phone(
            data['phone']) if user is None else self.validate_phone(user.phone)

        inventory = Inventory.create(data['areas'], inventorydate=data['inventorydate'],
                                     method=data['method'], visibility=data['visibility'],
                                     method_info=data['methodInfo'],
                                     attachments=data['attachments'],
                                     name=data['name'], email=data['email'], phone=data['phone'],
                                     more_info=data['moreInfo'], user=user)
        return inventory

    def add_edited_inventory(self, data, user):
        self.validate_missing_parameters(data)
        self.validate_coordinates(data['areas'])
        self.validate_inventorydate(data['inventorydate'])
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

    def validate_phone(self, phone):
        if phone == '':
            pass
        elif re.fullmatch(PHONE_REGEX, phone) is None:
            raise BadRequest(description='Invalid phone number.')

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
    
    def approve_edit(self, edit_id):
        edited_inv_json = self.get_edited_inventory(edit_id)
        original_inv_id = edited_inv_json['originalReport']
        original_inv = Inventory.objects.get({'_id': ObjectId(original_inv_id)})
        
        new_inv = self.inventory_json_to_object_format(edited_inv_json)
        self.__delete_areas(original_inv_id)
        areas = Inventory.create_areas(original_inv, self.__area_json_to_list(edited_inv_json['areas']))[1]
        Inventory.update_areas(original_inv, areas)

        try:
            Inventory.objects.raw({'_id': ObjectId(original_inv_id)}).update({"$set":new_inv})
            
        except:
            raise BadRequest(description='Invalid data')
        self.delete_edit(edit_id)
        return edited_inv_json

    def __area_json_to_list(self, areas):
        area_list = []
        
        for area in areas:
            area_list.append(area['coordinates'])
        
        return area_list

    def __delete_areas(self, id):
        try:
            Area.objects.raw({'inventory': ObjectId(id)}).delete()
        except (Area.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error

    def delete_edit(self, edit_id):
        try:
            EditedInventory.objects.raw({'_id': ObjectId(edit_id)}).delete()
        except (EditedInventory.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error

    def inventory_json_to_object_format(self, json):
        user = None
        if json['user']:
            user = User.objects.get({'_id': ObjectId(json['user']['id'])})
        
        return {
            'user': user,
            'method': json['method'],
            'visibility': json['visibility'],
            'method_info': json['methodInfo'],
            'attachments': json['attachments'],
            'name': json['name'],
            'email': json['email'],
            'phone': json['phone'],
            'more_info': json['moreInfo']
        }


inventory_service = InventoryService()
