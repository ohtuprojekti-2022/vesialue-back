from models.area import Area
from models.user import User
from models.inventory import Inventory

"""Methods and constants only used for unit testing."""
COORDINATES = [[{"lat": 60.17797731341533, "lng": 1.903111488320214},
                {"lat": 60.17473315099313, "lng": -24.886286597507773},
                {"lat": -70.17114712497474, "lng": 24.899506154574706}]]

TEST_REPORTS = [{
    "coordinates": COORDINATES,
    "inventorydate": "2021-02-22",
    "method": "other",
    "visibility": "",
    "methodInfo": "Voodoo magic",
    "attachments": False,
    "name": "Anna Annala",
    "email": "anna@hotmail.fi",
    "phone": "09 111222333",
    "moreInfo": "Hylyn näin, kun ohi kävelin."
},
    {
    "coordinates": COORDINATES,
    "inventorydate": "2020-02-22",
    "method": "dive",
    "visibility": "normal",
    "methodInfo": "",
    "attachments": True,
    "name": "Maija Maijala",
    "email": "hot_mail@hotmail.fi",
    "phone": "0449996666",
    "moreInfo": "Ei lisättävää."
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
