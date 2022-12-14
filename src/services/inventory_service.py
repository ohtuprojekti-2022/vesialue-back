import requests
from bson.objectid import ObjectId
from bson.errors import InvalidId
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized
from utils.config import BIG_DATA_API_KEY
from models.inventory import Inventory, AttachmentReference
from models.attachment import Attachment
from models.edited_inventory import EditedInventory
from models.area import Area
from models.delete_request import DeleteRequest
from services.validation import validation

# Disable pylint's no-member check since it causes unnecessary warnings when used with pymodm
# pylint: disable=no-member

class InventoryService:
    """ Class responsible for inventory logic."""

    def __init__(self):
        """ Class constructor. Creates a new inventory service."""

    def add_inventory(self, data, user, is_admin: bool = False):
        """Validates input data and adds a new inventory document to the database.

        Args:
            data (dict): Data containing inventory information.
            user (dict): User data.
            is_admin (bool, optional): True if user is admin. Defaults to False.

        Returns:
            list: List containing the created inventory and its areas as dictionaries.
        """
        self.validate_missing_parameters(data, False)
        validation.validate_coordinates(data['areas'])
        validation.validate_inventorydate_format(data['inventorydate'])
        validation.validate_inventorydate_date(data['inventorydate'])
        validation.validate_name(data['name'])
        validation.validate_method(data['method'])
        validation.validate_visibility(data['visibility'])
        validation.validate_method_info(data['method'], data['methodInfo'])
        validation.validate_more_info(data['moreInfo'])
        if user is None:
            validation.validate_email(data['email'])
            validation.validate_phone(data['phone'])
        else:
            validation.validate_email_loggedin(data['email'])
            validation.validate_phone_loggedin(data['phone'])
            validation.validate_email(user.email)
            validation.validate_phone(user.phone)

        city = self.get_city(self.get_center(data['areas']))

        inventory = Inventory.create(data['areas'], inventorydate=data['inventorydate'],
                                     method=data['method'], visibility=data['visibility'],
                                     city=city,
                                     method_info=data['methodInfo'],
                                     attachments=data['attachments'],
                                     name=data['name'], email=data['email'], phone=data['phone'],
                                     more_info=data['moreInfo'], user=user)

        inventory_report, areas = inventory
        inventory = self.get_inventory(inventory_report['id'], is_admin)

        return [inventory, areas]

    def add_edited_inventory(self, data, user):
        """Validates input data and creates a new edited inventory.

        Args:
            data (dict): Data for the new edited inventory.
            user (dict): User data.

        Raises:
            Unauthorized: If the user IDs on the original and edited inventory differ.

        Returns:
            dict: the newly created edited inventory object
        """
        self.validate_missing_parameters(data, True)
        validation.validate_coordinates(data['areas'])
        validation.validate_inventorydate_date(data['inventorydate'])
        validation.validate_method(data['method'])
        validation.validate_edit_reason(data['editReason'])
        self.validate_original_inventory_id(data['originalReport'])

        city = self.get_city(self.get_center(data['areas']))

        user_id_original = self.get_inventory(
            data['originalReport'])['user']['id']
        user_id_edited = str(user._id)
        if user_id_edited != user_id_original:
            raise Unauthorized(description='Authorization error')

        for item in EditedInventory.objects.all():
            itemjson = item.to_json()
            if str(itemjson['originalReport']) == str(data['originalReport']):
                item.delete()

        inventory = EditedInventory.create(data['areas'], inventorydate=data['inventorydate'],
                                           method=data['method'], visibility=data['visibility'],
                                           city=city,
                                           method_info=data['methodInfo'],
                                           edit_reason=data['editReason'],
                                           attachments=data['attachments'],
                                           more_info=data['moreInfo'],
                                           user=user,
                                           original_report=data['originalReport'])

        return inventory

    def get_inventory(self, inventory_id, is_admin: bool = False):
        inventory = None
        try:
            inventory = Inventory.objects.get({'_id': ObjectId(inventory_id)})
        except (Inventory.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error

        return inventory.to_json(hide_personal_info=not is_admin)

    def get_edited_inventory(self, inventory_id, is_admin=False):
        if is_admin is False:
            raise Unauthorized(description='Admin only')
        inventory = None
        try:
            inventory = EditedInventory.objects.get(
                {'_id': ObjectId(inventory_id)})
        except (EditedInventory.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error

        return inventory.to_json()

    def validate_original_inventory_id(self, id):
        try:
            self.get_inventory(id)
        except:
            raise BadRequest(description='Invalid original report id.')

    def validate_missing_parameters(self, data, edited):
        properties = [
            'areas',
            'inventorydate',
            'method',
            'visibility',
            'methodInfo',
            'attachments',
            'moreInfo'
        ]
        if not edited:
            properties += ['name', 'email', 'phone']

        for key in properties:
            if not key in data:
                raise BadRequest(description='Invalid request, missing '+key)

    def get_center(self, coordinates):
        max_lat = -90.0
        min_lat = 90.0
        max_lng = -180.0
        min_lng = 180.0

        for area in coordinates:
            for point in area:
                max_lat = max(point['lat'], max_lat)
                min_lat = min(point['lat'], min_lat)
                max_lng = max(point['lng'], max_lng)
                min_lng = min(point['lng'], min_lng)

        return ((max_lat + min_lat) / 2), ((max_lng + min_lng) / 2)

    def get_city(self, center):
        params = dict(
            latitude=center[0],
            longitude=center[1],
            localityLanguage='fi',
            key=BIG_DATA_API_KEY
        )

        url = 'https://api.bigdatacloud.net/data/reverse-geocode'
        response = requests.get(url=url, params=params, timeout=10).json()
        if not response['city'] or not response['locality']:
            return "Unknown location"
        if response['city'] != "":
            return f"{response['city']}, {response['locality']}"
        return response['locality']

    def get_areas(self):
        areas = []
        for area in Area.objects.all():
            areas.append(area.to_json())

        return areas

    def get_all_inventories(self, is_admin: bool = False):
        inventories = []
        for item in Inventory.objects.all().order_by([('inventorydate', -1)]):
            inventories.append(item.to_json(hide_personal_info=not is_admin))

        return inventories

    def get_all_edited_inventories(self, is_admin=False):
        if is_admin is False:
            raise Unauthorized(description='Admin only')
        inventories = []
        for item in EditedInventory.objects.all():
            inventories.append(item.to_json())

        return inventories

    def get_edited_inventories_by_user_id(self, user_id):
        inventories = []
        for item in EditedInventory.objects.raw({'user': {'$eq': ObjectId(user_id)}}):
            inventories.append(item.to_json())

        return inventories

    def approve_edit(self, edit_id, is_admin=False):
        if is_admin is False:
            raise Unauthorized(description='Admin only')

        edited_inv_json = self.get_edited_inventory(edit_id, is_admin)
        original_inv_id = edited_inv_json['originalReport']
        original_inv = Inventory.objects.get(
            {'_id': ObjectId(original_inv_id)})

        new_inv = self.inventory_json_to_object_format(edited_inv_json)
        self.__delete_areas(original_inv_id)
        areas, area_refs = Inventory.create_areas(
            original_inv, self.__area_json_to_list(edited_inv_json['areas']))
        Inventory.update_areas(original_inv, area_refs)

        try:
            Inventory.objects.raw(
                {'_id': ObjectId(original_inv_id)}).update({"$set": new_inv})
            self.delete_edit(edit_id, is_admin)
            updated_inventory = Inventory.objects.raw(
                {'_id': ObjectId(original_inv_id)})[0]
            return [updated_inventory.to_json(), areas]

        except:
            raise BadRequest(description='Invalid data')

    def __area_json_to_list(self, areas):  # pragma: no cover
        area_list = []

        for area in areas:
            area_list.append(area['coordinates'])

        return area_list

    def __delete_areas(self, id):  # pragma: no cover
        try:
            Area.objects.raw({'inventory': ObjectId(id)}).delete()
        except (Area.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error

    def delete_edit(self, edit_id, is_admin=False, user_id=None):
        try:
            edit_request = EditedInventory.objects.raw(
                {'_id': ObjectId(edit_id)})
            if not is_admin:
                if user_id is None or not user_id == edit_request[0].user._id:
                    raise Unauthorized(description='Admin only')
            edit_request.delete()
        except (EditedInventory.DoesNotExist, InvalidId, Unauthorized) as error:
            if isinstance(error, Unauthorized):
                raise error
            raise NotFound(description='404 not found') from error

    def delete_inventory(self, id, is_admin=False):
        if is_admin is False:
            raise Unauthorized(description='Admin only')
        try:
            attachments = Attachment.objects.raw({'inventory': ObjectId(id)})
            for attachment in attachments:
                attachment.file.delete()
            attachments.delete()
            Inventory.objects.raw({'_id': ObjectId(id)}).delete()
            self.__delete_areas(id)
        except (Inventory.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error

    def request_deletion(self, data, user):
        inventory = self.get_inventory(data['inventory'], user)
        if str(user._id) != inventory['user']['id']:
            raise Unauthorized(description='Authorization error')

        for item in DeleteRequest.objects.all():
            itemjson = item.to_json()
            if str(itemjson['inventory']) == str(data['inventory']):
                item.delete()

        delete_request = DeleteRequest.create(
            user, inventory['id'], data['reason'])
        return delete_request.to_json()

    def approve_deletion(self, request_id, is_admin):
        if is_admin is False:
            raise Unauthorized(description='Admin only')
        try:
            request = DeleteRequest.objects.get({'_id': ObjectId(request_id)})
        except (DeleteRequest.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error
        inventory_id = request.to_json()['inventory']
        self.delete_inventory(inventory_id, is_admin)
        self.remove_delete_request(request_id, is_admin, None)

    def remove_delete_request(self, request_id, is_admin, user_id=None):
        try:
            delete_request = DeleteRequest.objects.raw(
                {'_id': ObjectId(request_id)})
            if not is_admin:
                if user_id is None or (not delete_request[0].user._id == user_id):
                    raise Unauthorized(description='Admin only')
            delete_request.delete()
        except (DeleteRequest.DoesNotExist, InvalidId, Unauthorized) as error:
            if isinstance(error, Unauthorized):
                raise error
            raise NotFound(description='404 not found') from error

    def get_all_delete_requests(self, is_admin):
        if is_admin is False:
            raise Unauthorized(description='Admin only')
        delete_requests = []
        for item in DeleteRequest.objects.all():
            delete_requests.append(item.to_json())
        return delete_requests

    def get_delete_requests_by_user_id(self, user_id):
        inventories = []
        for item in DeleteRequest.objects.raw({'user': {'$eq': ObjectId(user_id)}}):
            inventories.append(item.to_json())

        return inventories

    def inventory_json_to_object_format(self, json):

        return {
            'method': json['method'],
            'visibility': json['visibility'],
            'city': json['city'],
            'method_info': json['methodInfo'],
            'attachments': json['attachments'],
            'more_info': json['moreInfo']
        }

    def add_attachment(self, inventory_id, attachment_files, user):
        # Get the inventory, return 404 if not found
        try:
            inventory = Inventory.objects.get(
                {'_id': ObjectId(inventory_id)})
        except (Inventory.DoesNotExist, InvalidId) as error:
            raise NotFound(description='invalid inventory') from error

        # Check if user owns the inventory
        if str(user._id) != str(inventory.user._id):
            return {'invalid user', 400}

        # Get current attachment files
        references = inventory.attachment_files

        # Check that max. 5 attachment files are allowed
        if (len(references) + len(attachment_files)) > 5:
            return {'too many attachments', 400}

        # Get attachments from the form
        attachments = []
        for file in attachment_files:
            file.name = file.filename
            attachment = Attachment(file=file, inventory=inventory)
            attachment.save()
            attachments.append(attachment)

        # Append references of the new attachment files to the inventory
        for attachment in attachments:
            references.append(AttachmentReference.create(attachment))
        inventory.attachment_files = references

        # Set attachments boolean to true if it's not yet set
        if not inventory.attachments:
            inventory.attachments = True

        inventory.save()

        # Return attachment files as json
        return [reference.to_json() for reference in references]

    def delete_attachment(self, attachment_id, user, is_admin):
        # Get the attachment object from mongo
        try:
            attachment = Attachment.objects.get(
                {'_id': ObjectId(attachment_id)}
            )
        except (Attachment.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error

        # Get the inventory associated with the attachment
        try:
            inventory = Inventory.objects.get(
                {'_id': ObjectId(attachment.inventory._id)}
            )
        except (Inventory.DoesNotExist, InvalidId) as error:
            raise NotFound(description='404 not found') from error


        # Check if user matches the inventory's user OR user is admin
        if is_admin or str(user._id) == str(inventory.user._id):
            # Delete the attachment, included file data and reference from the report
            try:
                references = inventory.attachment_files
                # Delete reference from the inventory
                for ref in references:
                    if str(ref.attachment._id) == str(attachment_id):
                        references.remove(ref)
                inventory.attachment_files = references

                # Set attachments boolean to false if no remaining references
                if not references or len(references) == 0:
                    inventory.attachments = False

                inventory.save()

                # Delete file data
                attachment.file.delete()

                # Delete attachment object
                Attachment.objects.raw({'_id': ObjectId(attachment_id)}).delete()
            except (Attachment.DoesNotExist, InvalidId) as error:
                raise NotFound(description='404 not found') from error
        else:
            return {'error': 'bad request'}, 400

        return {'deleted': attachment_id}, 200

inventory_service = InventoryService()
# pylint: enable=no-member
