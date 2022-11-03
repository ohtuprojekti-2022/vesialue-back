import jwt
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash, generate_password_hash
from pymodm import errors
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

        if self.user_exists_by_field("username", username):
            raise BadRequest(description='Username already exists.')
        if self.user_exists_by_field("email", email):
            raise BadRequest(description='Email already exists.')

        user = User.create(username=username, password=password,
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

    def edit(self, user_data):
        validation.validate_password(user_data['password'])
        validation.validate_email(user_data['email'])
        validation.validate_phone(user_data['phone'])

        password_hash = generate_password_hash(user_data['password'])
        username = user_data['username']

        User.objects.raw({"username": username}).update({"$set": {"email": user_data['email'],
                                                                  "phone": user_data['phone'],
                                                                  "name": user_data['name'],
                                                                  "password": password_hash}})

        user = User.objects.raw({'username': {'$eq': username}}).first()
        user_json = user.to_json()

        return {'auth': self.generate_token(user_json), 'user': user_json}

    def generate_token(self, user_json):
        return jwt.encode({'user_id': user_json['id']}, SECRET_KEY)

    def user_exists_by_field(self, field, value):
        try:
            User.objects.raw({
                field: {'$eq': value}
            }).first()
        except (errors.DoesNotExist, errors.ModelDoesNotExist):
            return False
        return True

user_service = UserService()
