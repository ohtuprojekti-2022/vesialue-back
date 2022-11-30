import re
import datetime
from werkzeug.exceptions import BadRequest

COORDINATE_REGEX = r"\{'lat': -?[1-9]?[0-9].\d{10,15}, 'lng': -?(1[0-7]?[0-9]|[1-7]?[0-9]|180).\d{10,15}\}"
EMAIL_REGEX = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
PHONE_REGEX = r'^\+?(?:[0-9][ |-]?){6,14}[0-9]$'


class Validation:
    """ Class responsible for validation logic."""

    def validate_password(self, password):
        if len(password) < 10:
            raise BadRequest(description='Password too short.')
        if len(password) > 100:
            raise BadRequest(description='Password too long.')

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
        if len(email) > 100:
            raise BadRequest(description='Email too long.')

    def validate_phone(self, phone):
        if re.fullmatch(PHONE_REGEX, phone) is None and phone != '':
            raise BadRequest(description='Invalid phone number.')

    def validate_name(self, name):
        if len(name) > 100:
            raise BadRequest(description='Invalid name.')

    def validate_method_info(self, method, method_info):
        if method == 'other':
            if len(method_info) > 100:
                raise BadRequest(description='Method info too long.')
            if method_info == "":
                raise BadRequest(description='No method info given.')

    def validate_more_info(self, more_info):
        if len(more_info) > 500:
            raise BadRequest(description='Info too long.')

    def validate_edit_reason(self, edit_reason):
        if len(edit_reason) < 1:
            raise BadRequest(description='No reason for edit.')
        if len(edit_reason) > 500:
            raise BadRequest(description='Reason for edit too long.')


validation = Validation()
