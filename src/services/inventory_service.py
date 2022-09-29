import re
import datetime
from werkzeug.exceptions import BadRequest
from pymodm import errors
from models.inventory import Inventory

COORDINATE_REGEX = '^[NS]([0-8][0-9](\.[0-5]\d){2}|90(\.00){2})\040[EW]((0\d\d|1[0-7]\d)(\.[0-5]\d){2}|180(\.00){2})$'
EMAIL_REGEX = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'

class InventoryService:
    """ Class responsible for inventory logic."""
    
    def __init__(self):
        """ Class constructor. Creates a new sight service."""

    def add_inventory(self, data):
        coordinates = data['coordinates']
        inventorydate = data['inventorydate']
        method = data['method']
        attachments = data['attachments']
        name = data['name']
        email = data['email']
        phone = data['phone']
        more_info = data['more_info']
        
        self.validate_inventorydate(inventorydate)
        self.validate_method(method)
        self.validate_email(email)
    
        inventory = Inventory.create(coordinates=coordinates, inventorydate=inventorydate, method=method,
            		  attachments=attachments, name=name, email=email, phone=phone, more_info=more_info)
    
        return inventory.to_json()
    
    def validate_inventorydate(self, inventorydate):
        try:
            datetime.datetime.strptime(inventorydate, '%Y-%m-%d')
        except ValueError:
            raise BadRequest(description='Invalid date.')
    
    def validate_method(self, method):
        if method not in ["Näköhavainto", "Viistokaiutus", "Sukellus", "Muu, mikä?"]:
            raise BadRequest(description='Invalid method.')

    def validate_email(self, email):
        if re.fullmatch(EMAIL_REGEX, email) is None:
            print('jee')
            raise BadRequest(description='Invalid email.')
            
inventory_service = InventoryService()
