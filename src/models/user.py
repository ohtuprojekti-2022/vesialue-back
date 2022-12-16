from pymodm import MongoModel, fields

class User(MongoModel):
    """Class that represents a user.
    Attributes:
        username: [String] User's username.
        password: [String] Hashed password.
        name: [String] Name of the user. Not required.
        email: [String] User's e-mail address.
        phone: [String] User's phonenumber. Not required.
        admin: [Integer] Admin status as integer. 
            0 = not admin, 1= admin, 2 = super admin. 0 by default.
    """
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
    def create(username, password_hash, name, email, phone):
        user = User(username, password_hash, name, email, phone, admin=0)
        user.save()
        return user

    def set_admin(self, admin_level):
        self.admin = admin_level
        self.save()

    def is_admin(self) -> bool:
        return self.admin == 1

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
