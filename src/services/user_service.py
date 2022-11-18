import jwt
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash, generate_password_hash
from pymodm import errors
from bson.objectid import ObjectId
from models.user import User
from services.validation import validation
from utils.config import SECRET_KEY

class UserService:
    """ Class responsible for user logic."""

    def __init__(self):
        """ Class constructor. Creates a new user service."""

    def create_user(self, data):
        password = data['password']
        name = data['name']
        email = data['email']
        phone = data['phone']
        username = data['username']

        validation.validate_password(password)
        validation.validate_email(email)
        validation.validate_phone(phone)
        validation.validate_username(username)
        validation.validate_name(name)

        if self.user_exists_by_field("username", username):
            raise BadRequest(description='Username already exists.')
        if self.user_exists_by_field("email", email):
            raise BadRequest(description='Email already exists.')

        password_hash = generate_password_hash(password)

        user = User.create(username=username, password_hash=password_hash,
                           name=name, email=email, phone=phone)

        return user.to_json()

    def login_user(self, username, password):
        # Username and password length validation
        if len(username) > 32 or len(username) < 3 or len(password) < 10 or len(password) > 128:
            raise BadRequest(description='Invalid username or password.')

        # Check if user exists in the database
        try:
            user = User.objects.raw({
                'username': {'$eq': username}
            }).first()
        except (errors.DoesNotExist, errors.ModelDoesNotExist) as error:
            raise BadRequest(description='Invalid username or password.') from error

        # Validate user password hash
        if not check_password_hash(user.password, password):
            raise BadRequest(description='Invalid username or password.')
        user_json = user.to_json()

        return {'auth': self.generate_token(user_json), 'user': user_json}

    def set_admin(self, username, admin_level):
        user = User.objects.raw({'username': {'$eq': username}}).first()
        user.set_admin(admin_level)
        user_json = user.to_json()
        return {'auth': self.generate_token(user_json), 'user': user_json}

    def check_admin(self, headers: dict) -> bool:
        token = self.get_token(headers)
        if token is not None and token['admin'] == "1":
            return True
        return False

    def edit(self, user, user_data):
        username = user.username

        if username != user_data['username']:
            validation.validate_username(user_data['username'])
            if self.user_exists_by_field("username", user_data['username']):
                raise BadRequest(description='Username already exists.')
        if user.email != user_data['email']:
            validation.validate_email(user_data['email'])
            if self.user_exists_by_field("email", user_data['email']):
            	raise BadRequest(description='Email already exists.')
        validation.validate_phone(user_data['phone'])
        validation.validate_name(user_data['name'])

        User.objects.raw({"username": username}).update({"$set": {"username": user_data['username'], "email": user_data['email'],
                                                                  "phone": user_data['phone'],
                                                                  "name": user_data['name']}})

        user = User.objects.raw({'username': {'$eq': user_data['username']}}).first()
        user_json = user.to_json()

        return {'auth': self.generate_token(user_json), 'user': user_json}

    def edit_password(self, user, old_password, new_password):
        username = user.username

        if not check_password_hash(user.password, old_password):
            raise BadRequest(description='Invalid current password.')

        validation.validate_password(new_password)
        password_hash = generate_password_hash(new_password)

        User.objects.raw({"username": username}).update({"$set": {"password": password_hash}})

        user = User.objects.raw({'username': {'$eq': username}}).first()
        user_json = user.to_json()

        return {'auth': self.generate_token(user_json), 'user': user_json}

    def generate_token(self, user_json):
        return jwt.encode({'user_id': user_json['id'], 'admin': user_json['admin']}, SECRET_KEY)

    def user_exists_by_field(self, field, value):
        try:
            User.objects.raw({
                field: {'$eq': value}
            }).first()
        except (errors.DoesNotExist, errors.ModelDoesNotExist):
            return False
        return True

    def get_token(self, headers: dict) -> dict:
        if 'Authorization' in headers:
            token = str.replace(str(headers['Authorization']), 'Bearer ', '')
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            if not decoded_token['user_id'] or not decoded_token['admin']:
                raise BadRequest(description='Authorization token missing or invalid')
            return decoded_token
        return None

    def check_authorization(self, headers: dict) -> User:
        token = self.get_token(headers)
        if token is not None:
            return User.objects.get({'_id': ObjectId(token['user_id'])})
        return None

user_service = UserService()
