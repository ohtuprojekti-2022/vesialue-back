from pymodm import MongoModel, fields
from werkzeug.security import generate_password_hash


class User(MongoModel):
    _id = fields.ObjectId()
    username = fields.CharField(required=True, min_length=3)
    password = fields.CharField(required=True, min_length=10)
    name = fields.CharField(blank=True)
    email = fields.CharField()
    phone = fields.CharField(blank=True)
    admin = fields.IntegerField(required=True, default=0)

    class Meta:
        '''Defines MongoDB options for this model'''
        connection_alias = 'app'
        final = True

    @staticmethod
    def create(username, password, name, email, phone):
        user = User(username, generate_password_hash(
            password), name, email, phone, admin=False)
        user.save()
        return user

    def set_admin(self, admin_level):
        self.admin = admin_level
        self.save()

    def to_json(self):
        return {
            'id': str(self._id),
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'username': self.username,
            'admin': str(self.admin)
        }
