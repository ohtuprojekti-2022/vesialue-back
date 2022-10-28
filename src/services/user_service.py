import re
import jwt
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash
from pymodm import errors
from models.user import User
from utils.config import SECRET_KEY

EMAIL_REGEX = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
PHONE_REGEX = r'^((04[0-9]{1})(\s?|-?)|050(\s?|-?)|0457(\s?|-?)|[+]?358(\s?|-?)50|0358(\s?|-?)50|00358(\s?|-?)50|[+]?358(\s?|-?)4[0-9]{1}|0358(\s?|-?)4[0-9]{1}|00358(\s?|-?)4[0-9]{1})(\s?|-?)(([0-9]{3,4})(\s|\-)?[0-9]{1,4})$'


def generate_token(user):
    return jwt.encode({'user_id': user['id']}, SECRET_KEY)

def user_exists_by_field(field, value):
    # pylint: disable=no-member
    try:
        User.objects.raw({
            field: {'$eq': value}
        }).first()
    except (errors.DoesNotExist, errors.ModelDoesNotExist):
        return False
    return True
    # pylint: enable=no-member

def create_user(data):
    password = data['password']
    if len(password) < 10:
        raise BadRequest(description='password too short')

    email = data['email']
    if re.fullmatch(EMAIL_REGEX, email) is None:
        raise BadRequest(description='email is not valid')

    phone = data['phone']
    if phone == '':
        pass
    elif re.fullmatch(PHONE_REGEX, phone) is None:
        raise BadRequest(description='phone number is not valid')

    name = data['name']

    username = data['username']
    if len(username) < 3:
        raise BadRequest(description='username too short')

    if len(username) > 32:
        raise BadRequest(description='username too long')

    if user_exists_by_field("username", username):
        raise BadRequest(description='username taken')

    if user_exists_by_field("email", email):
        raise BadRequest(description='email taken')

    user = User.create(username=username, password=password,
                           name=name, email=email, phone=phone)
    return user.to_json()


def login_user(username, password):
    # Username and password length validation
    if len(username) > 32 or len(username) < 3 or len(password) < 10 or len(password) > 128:
        raise BadRequest(description='incorrect username or password')

    # Check if user exists in the database
    # pylint: disable=no-member
    try:
        user = User.objects.raw({
            'username': {'$eq': username}
        }).first()
    except (errors.DoesNotExist, errors.ModelDoesNotExist) as error:
        raise BadRequest(description='incorrect username or password') from error
    # pylint: enable=no-member

    # Validate user password hash
    if not check_password_hash(user.password, password):
        raise BadRequest(description='incorrect username or password')
    user = user.to_json()
    return {'auth': generate_token(user), 'user': user}
