import re
from werkzeug.exceptions import BadRequest
from pymodm import errors
from models.user import User

EMAIL_REGEX = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'


def create_user(data):
    password = data['password']
    if len(password) < 10:
        raise BadRequest(description='password too short')

    email = data['email']
    if re.fullmatch(EMAIL_REGEX, email) is None:
        raise BadRequest(description='email is not valid')

    phone = data['phone']
    name = data['name']

    username = data['username']
    if len(username) < 3:
        raise BadRequest(description='username too short')
    user = None
    try:
        user = User.objects.raw({
            'username': {'$eq': username}
        }).first()
        raise BadRequest(description='username taken')
    except (errors.DoesNotExist, errors.ModelDoesNotExist):
        user = User.create(username=username, password=password,
                       name=name, email=email, phone=phone)
    return user.to_json()

def login_user(data):
    username = data['username']
    password = data['password']
    
    if username is None or password is None:
        # error
    
    try:
        user = User.objects.raw({
            'username': {'$eq': username}
        }).first()
    except (errors.DoesNotExist, errors.ModelDoesNotExist):
        raise BadRequest(description='user not found')
    
    return user.to_json()    