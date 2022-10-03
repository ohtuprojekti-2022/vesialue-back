from pymodm import EmbeddedMongoModel, MongoModel, fields


class Point(EmbeddedMongoModel):
    lat = fields.CharField(required=True)
    long = fields.CharField(required=True)

    class Meta:
        connection_alias = 'app'
        final = True

    @staticmethod
    def create(lat_lng):
        return Point(lat_lng['lat'], lat_lng['lng'])

    def to_json(self):
        return {
            'lat': str(self.lat),
            'long': str(self.long)
        }


class Area(MongoModel):
    _id = fields.ObjectId()
    inventory = fields.ReferenceField('Inventory')
    coordinates = fields.EmbeddedDocumentListField(Point)

    class Meta:
        connection_alias = 'app'
        final = True

    @staticmethod
    def create(inventory, coordinates):
        coordinate_points = []
        for lat_lng in coordinates:
            coordinate_points.append(Point.create(lat_lng))
        area = Area(inventory, coordinates=coordinate_points)
        return area.save()

    def to_json(self, simple=False):
        coordinates = []
        for point in self.coordinates:
            coordinates.append(point.to_json())
        if simple:
            return coordinates
        return {
            'id': str(self._id),
            'inventory': str(self.inventory),
            'coodinates': coordinates
        }
