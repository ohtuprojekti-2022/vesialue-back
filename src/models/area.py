from pymodm import EmbeddedMongoModel, MongoModel, fields


class Point(EmbeddedMongoModel):
    """Class that represents a point on a map.
    Attributes:
        lat: [Float] Latitude coordinate.
        long: [Float] Longitude coordinate.
    """
    lat = fields.FloatField(required=True)
    long = fields.FloatField(required=True)

    class Meta:
        connection_alias = 'app'
        final = True

    @staticmethod
    def create(lat_lng):
        return Point(lat_lng['lat'], lat_lng['lng'])

    def to_json(self):
        return {
            'lat': self.lat,
            'lng': self.long
        }


class Area(MongoModel):
    """Class that represents an area.
    Attributes:
        inventory: [INVENTORY] The inventory that the area belongs to.
        coordinates: [POINT] List of coordinates as points.
    """
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
            'inventoryId': str(self.inventory._id),
            'coordinates': coordinates
        }
