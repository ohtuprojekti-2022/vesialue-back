import re
import jwt
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash
from pymodm import errors
from models.user import User
from utils.config import SECRET_KEY

EMAIL_REGEX = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'


def generate_token(user):
    return jwt.encode({'user_id': user['id']}, SECRET_KEY)


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


def login_user(username, password):
    # Username and password length validation
    if len(username) > 32 or len(username) < 3 or len(password) < 10 or len(password) > 128:
        raise BadRequest(description='incorrect username or password')

    # Check if user exists in the database
    try:
        user = User.objects.raw({
            'username': {'$eq': username}
        }).first()
    except (errors.DoesNotExist, errors.ModelDoesNotExist):
        raise BadRequest(description='incorrect username or password')

    # Validate user password hash
    if not check_password_hash(user.password, password):
        raise BadRequest(description='incorrect username or password')
    user = user.to_json()
    return {'auth': generate_token(user), 'user': user}
