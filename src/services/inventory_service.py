import re
from werkzeug.exceptions import BadRequest
from pymodm import errors
from models.inventory import Inventory

EMAIL_REGEX = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'

def add_inventory(data):
    coordinates = data['coordinates']
    inventorydate = data['inventorydate']
    method = data['method']
    attachments = data['attachments']
    name = data['name']
    email = data['email']
    phone = data['phone']
    more_info = data['more_info']

    inventory = Inventory.create(coordinates=coordinates, inventorydate=inventorydate, method=method,
        		  attachments=attachments, name=name, email=email, phone=phone, more_info=more_info)

    return inventory.to_json()
