import unittest
from models.edited_inventory import EditedInventory
import tests.test_tools as tt
from models.user import User
from models.inventory import Inventory
from utils.mongo import connect_to_db
from services.inventory_service import InventoryService
import re

connect_to_db()


class TestEditedInventory(unittest.TestCase):
    def setUp(self):
        tt.delete_all_edited_inventories()
        self.user = User.create(username="testikäyttäjä",
                                password="1234qwer",
                                name="Inven Tory",
                                email="inventory@gmail.com",
                                phone="040777888999")

        self.inventory = Inventory.create(tt.COORDINATES,
                                          user=self.user,
                                          inventorydate="1988-03-12",
                                          method="dive",
                                          visibility="normal",
                                          method_info="",
                                          attachments=True,
                                          name="",
                                          email="",
                                          phone="",
                                          more_info="Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtää kuvat ulkomuistista.")[0]

    def test_create_edited_inventory(self):
        edited_inventory = EditedInventory.create(tt.COORDINATES_EDITED,
                                                  user=self.user,
                                                  inventorydate="1988-03-13",
                                                  method="dive",
                                                  visibility="normal",
                                                  method_info="",
                                                  edit_reason="Päivämäärä oli väärin",
                                                  attachments=True,
                                                  more_info="Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtää kuvat ulkomuistista.",
                                                  original_report=self.inventory["id"])
        self.assertEqual(
            edited_inventory['areas'][0]['coordinates'], tt.COORDINATES_EDITED[0])
        self.assertEqual(edited_inventory['user'], self.user.to_json())
        self.assertEqual(edited_inventory['inventorydate'], '1988-03-13')
        self.assertEqual(edited_inventory['method'], "dive")
        self.assertEqual(edited_inventory['visibility'], "normal")
        self.assertEqual(edited_inventory['methodInfo'], "")
        self.assertEqual(edited_inventory['editReason'], "Päivämäärä oli väärin")
        self.assertEqual(edited_inventory['attachments'], True)
        self.assertEqual(
            edited_inventory['moreInfo'], "Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtää kuvat ulkomuistista.")
        self.assertEqual(
            edited_inventory['originalReport'], self.inventory["id"])
