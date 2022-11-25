from models.area import Area
from models.user import User
from models.inventory import Inventory
from models.edited_inventory import EditedInventory
from models.delete_request import DeleteRequest

"""Methods and constants only used for testing."""
USERS = [{
	"username": "testaaja",
	"password": "sanasala123?",
	"name": "Hanna Hannala",
	"email": "hanna@sposti.fi",
	"phone": "+358457385576",
	"admin": "0"
}]

COORDINATES = [[{"lat": 60.17797731341533, "lng": 1.903111488320214},
                {"lat": 60.17473315099313, "lng": -24.886286597507773},
                {"lat": -70.17114712497474, "lng": 24.899506154574706}]]

COORDINATES_EDITED = [[{"lat": 62.17797731353904, "lng": 5.003321488390214},
                {"lat": 60.17473315099313, "lng": -24.886286597507773},
                {"lat": -70.17114712497474, "lng": 24.899506154574706}]]

TEST_REPORTS = [{
    "areas": COORDINATES,
    "inventorydate": "2021-02-22",
    "method": "other",
    "visibility": "",
    "methodInfo": "Voodoo magic",
    "attachments": False,
    "name": "Anna Annala",
    "email": "anna@hotmail.fi",
    "phone": "0457387750",
    "moreInfo": "Hylyn näin, kun ohi kävelin."
},
    {
    "areas": COORDINATES,
    "inventorydate": "2020-02-22",
    "method": "dive",
    "visibility": "normal",
    "methodInfo": "",
    "attachments": True,
    "name": "Maija Maijala",
    "email": "hot_mail@hotmail.fi",
    "phone": "0458669978",
    "moreInfo": "Ei lisättävää."
},
    {
    "areas": COORDINATES,
    "inventorydate": "1988-12-12",
    "method": "dive",
    "visibility": "normal",
    "methodInfo": "",
    "attachments": False,
    "name": "",
    "email": "hanna@sposti.fi",
    "phone": "",
    "moreInfo": "Sumuista."
}]


def get_all_users():
    try:
        users = User.objects.all()
        return users
    except User.DoesNotExist:
        return None


def delete_all_users():
    users = get_all_users()
    if users:
        for user in users:
            user.delete()


def get_all_inventories():
    try:
        inventories = Inventory.objects.all()
        return inventories
    except Inventory.DoesNotExist:
        return None


def delete_all_inventories():
    try:
        Inventory.objects.all().delete()
        Area.objects.all().delete()
    except:
        pass

def delete_all_edited_inventories():
    try:
        EditedInventory.objects.all().delete()
    except:
        pass

def delete_all_delete_requests():
    try:
        DeleteRequest.objects.all().delete()
    except:
        pass
