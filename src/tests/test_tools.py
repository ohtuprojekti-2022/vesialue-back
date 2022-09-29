from models.user import User
from models.inventory import Inventory

"""Methods only used for unit testing."""
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
    inventories = get_all_inventories()
    if inventories:
        for inventory in inventories:
            inventory.delete()
