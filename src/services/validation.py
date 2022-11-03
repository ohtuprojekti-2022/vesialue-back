import re
import datetime
from werkzeug.exceptions import BadRequest

COORDINATE_REGEX = r"\{'lat': -?[1-9]?[0-9].\d{10,15}, 'lng': -?(1[0-7]?[0-9]|[1-7]?[0-9]|180).\d{10,15}\}"
EMAIL_REGEX = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
PHONE_REGEX = r'^((04[0-9]{1})(\s?|-?)|050(\s?|-?)|0457(\s?|-?)|[+]?358(\s?|-?)50|0358(\s?|-?)50|00358(\s?|-?)50|[+]?358(\s?|-?)4[0-9]{1}|0358(\s?|-?)4[0-9]{1}|00358(\s?|-?)4[0-9]{1})(\s?|-?)(([0-9]{3,4})(\s|\-)?[0-9]{1,4})$'

class Validation:
    """ Class responsible for validation logic."""

    def validate_password(self, password):
        if len(password) < 10:
            raise BadRequest(description='Password too short.')

    def validate_username(self, username):
        if len(username) < 3:
            raise BadRequest(description='Username too short.')
        if len(username) > 32:
            raise BadRequest(description='Username too long.')

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
        if re.fullmatch(PHONE_REGEX, phone) is None and phone != '':
            raise BadRequest(description='Invalid phone number.')

    def validate_method_info(self, method, method_info):
        if method == 'other':
            if len(method_info) > 100:
                raise BadRequest(description='Method info too long.')
            if method_info == "":
                raise BadRequest(description='No method info given.')

    def validate_more_info(self, more_info):
        if len(more_info) > 500:
            raise BadRequest(description='Info too long.')

validation = Validation()
