import unittest
from unittest.mock import Mock, ANY, MagicMock
from services.inventory_service import InventoryService

class TestInventoryService(unittest.TestCase):
    def setUp(self):
        self.inventory_repo_mock = Mock()
        self.invs = InventoryService(self.inventory_repo_mock)

    def test_add_inventory(self):
        self.inventory_repo_mock.add_inventory.return_value = True
        self.invs = InventoryService(self.inventory_repo_mock)
        return_value = self.invs.add_inventory("Heikki Heikkinen", "heiki_@helsinki.fi", "044 987654", "Etaisyyksiin kaytetty 3D-skanneria")
        self.assertEqual(return_value, (True, "Lahetys onnistui."))

    def test_add_inventory_with_fail(self):
        self.inventory_repo_mock.add_inventory.return_value = False
        self.rs = InventoryService(self.inventory_repo_mock)
        return_value = self.rs.add_inventory("Minna Minnanen", "minna78@helsinki.fi", "044 9677777", "-")
        self.assertEqual(return_value, (False, "Lahetys ei onnistunut."))
        

