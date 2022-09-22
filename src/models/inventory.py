from pymodm import MongoModel, fields

class Inventory(MongoModel):
    """ Class that represents a single inventory.
        Attributes:
            name: [String] The name of the submitter.
            email: [String] The email of the submitter.
            phonenumber: [String] The phonenumber of the submitter.
            coordinates: [String] Coordinates of the inventory area.
            time: [String] Time of the inventory.
            methods: [String] Type of methods used in the inventory.
            attachments: [boolean] True if there are attachments included.
            other: [String] Other notes for the inventory.
    """

    coordinates = fields.CharField(required=True)
    time = fields.DateTimeField(required=True)
    methods = fields.CharField(required=True)
    attachments = fields.BooleanField(required=True, default=False)
    name = fields.CharField(blank=True)
    email = fields.CharField(blank=True)
    phonenumber = fields.CharField(blank=True)
    other = fields.CharField(blank=True)

    class Meta:
        connection_alias = 'app'
        final = True

    @staticmethod
    def create(coordinates, time, methods, attachments, name="", email="", phonenumber="", other=""):
        inventory = Inventory(coordinates, time, methods, attachments, name, email, phonenumber, other)
        inventory.save()
        return inventory

    def to_json(self):
        return {
            'coordinates': self.coordinates,
            'time': str(self.time),
            'methods': str(self.methods),
            'attachments': str(self.attachments),
            'name': str(self.name),
            'email': str(self.email),
            'phonenumber': str(self.phonenumber),
            'other': str(self.other)
        }
    