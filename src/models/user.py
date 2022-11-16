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
            password), name, email, phone, admin=0)
        user.save()
        return user

    def set_admin(self, admin_level):
        self.admin = admin_level
        self.save()

    def is_admin(self) -> bool:
        return True if self.admin == 1 else False

    def to_json(self, hide_personal_info: bool = False):
        user_email = "" if hide_personal_info else str(self.email)
        user_phone = "" if hide_personal_info else str(self.phone)

        return {
            'id': str(self._id),
            'name': self.name,
            'email': user_email,
            'phone': user_phone,
            'username': self.username,
            'admin': str(self.admin)
        }
