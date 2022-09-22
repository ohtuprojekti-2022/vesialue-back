from pymodm import MongoModel, fields

class Inventory(MongoModel):
    """ Class that represents a single inventory.
        Attributes:
            coordinates: [String] Coordinates of the inventory area.
            inventorydate: [String] Time of the inventory.
            method: [String] Type of the method used in the inventory.
            attachments: [boolean] True if there are attachments included.
            name: [String] The name of the submitter.
            email: [String] The email of the submitter.
            phone: [String] The phonenumber of the submitter.
            other: [String] Other notes for the inventory.
    """

    coordinates = fields.CharField(required=True)
    inventorydate = fields.DateTimeField(required=True)
    method = fields.CharField(required=True)
    attachments = fields.BooleanField(required=True, default=False)
    name = fields.CharField(blank=True)
    email = fields.CharField(blank=True)
    phone = fields.CharField(blank=True)
    other = fields.CharField(blank=True)

    class Meta:
        connection_alias = 'app'
        final = True

    @staticmethod
    def create(coordinates, inventorydate, method, attachments, name="", email="", phone="", other=""):
        inventory = Inventory(coordinates, iventorydate, method, attachments, name, email, phone, other)
        inventory.save()
        return inventory

    def to_json(self):
        return {
            'coordinates': self.coordinates,
            'inventorydate': str(self.inventorydate),
            'method': str(self.method),
            'attachments': str(self.attachments),
            'name': str(self.name),
            'email': str(self.email),
            'phone': str(self.phone),
            'other': str(self.other)
        }
    
