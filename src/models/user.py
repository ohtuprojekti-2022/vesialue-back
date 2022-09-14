from pymodm import MongoModel, fields
from werkzeug.security import generate_password_hash

class User(MongoModel):
    username = fields.CharField(required=True, min_length=3)
    password = fields.CharField(required=True, min_length=10)
    name = fields.CharField()
    email = fields.CharField()
    phone = fields.CharField()
    
    class Meta:
        connection_alias = 'app'
        final = True
    
    @staticmethod
    def create(username, password, name, email, phone):
        user = User(username, generate_password_hash(password), name, email, phone)
        user.save()
        return user
    
    