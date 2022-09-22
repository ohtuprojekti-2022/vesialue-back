import re
from werkzeug.exceptions import BadRequest
from pymodm import errors
from models.inventory import Inventory

EMAIL_REGEX = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'

def add_inventory(data):
    coordinates = data['coordinates']
    time = data['time']
    methods = data['methods']
    attachments = data['attachments']
    name = data['name']
    email = data['email']
    phonenumber = data['phonenumber']
    other = data['other']

    inventory = Inventory.create(coordinates=coordinates, time=time, methods=methods,
        		  attachments=attachments, name=name, email=email, phonenumber=phonenumber, other=other)

    return inventory.to_json()
