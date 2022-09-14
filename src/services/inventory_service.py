from src.entities.inventory import Inventory
from src.repositories.inventory_repository import inventory_repository as default_inventory_repository

class InventoryService:
    """ Class responsible for inventory logic."""

    def __init__(self, inventory_repository=default_inventory_repository):
        """ Class constructor. Creates a new inventory service.
        Args:"""

        self._inventory = None
        self._inventory_repository = inventory_repository

    def add_inventory(self, name, email, phonenumber, coordinates, time, methods, attachments, other):
        """ Adds a new inventory."""

        if coordinates == "" or time == "" or methods == "":
            return False, "Tayta kaikki tiedot"

        self._inventory = Inventory(name, email, phonenumber, coordinates, time, methods, attachments, other)

        if self._inventory_repository.add_inventory(self._inventory):
            return True, "Lahetys onnistui."

        return False, "Lahetys ei onnistunut."

inventory_service = InventoryService()
