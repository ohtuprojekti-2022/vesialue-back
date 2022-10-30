import unittest
import re
import datetime
import tests.test_tools as test_tools
from models.area import Area
from models.user import User
from utils.mongo import connect_to_db
from models.inventory import Inventory
from tests.test_tools import COORDINATES

connect_to_db()


class TestInventory(unittest.TestCase):
    def setUp(self):
        test_tools.delete_all_users()
        self.user = User.create(username="testikäyttäjä",
                    password="1234qwer",
                    name="Inven Tory",
                    email="inventory@gmail.com",
                    phone="040777888999")

    def test_create_inventory_with_user(self):
        inventory = Inventory.create(COORDINATES,
        							 user=self.user,
        							 inventorydate="1988-03-12",
                                     method="dive",
                                     visibility="normal",
                                     method_info="",
                                     attachments=True,
                                     name="",
                                     email="",
                                     phone="",
                                     more_info="Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtaa kuvat ulkomuistista.")[0]

        assert re.match(r'[0-9a-f]{24}', inventory['areas'][0]['area'])
        self.assertEqual(inventory['user'], self.user.to_json())
        self.assertEqual(inventory['inventorydate'], '1988-03-12')
        self.assertEqual(inventory['method'], "dive")
        self.assertEqual(inventory['visibility'], "normal")
        self.assertEqual(inventory['methodInfo'], "")
        self.assertEqual(inventory['attachments'], True)
        self.assertEqual(inventory['name'], "")
        self.assertEqual(inventory['email'], "")
        self.assertEqual(inventory['phone'], "")
        self.assertEqual(
            inventory['moreInfo'], "Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtaa kuvat ulkomuistista.")

    def test_create_inventory_without_user(self):
        inventory = Inventory.create(COORDINATES,
							 user=None,
							 inventorydate="1987-03-12",
                             method="dive",
                             visibility="normal",
                             method_info="",
                             attachments=False,
                             name="Matti Mattinen",
                             email="matti@sposti.fi",
                             phone="050556677",
                             more_info="Ei ole..")[0]

        assert re.match(r'[0-9a-f]{24}', inventory['areas'][0]['area'])
        self.assertEqual(inventory['user'], None)
        self.assertEqual(inventory['inventorydate'], '1987-03-12')
        self.assertEqual(inventory['method'], "dive")
        self.assertEqual(inventory['visibility'], "normal")
        self.assertEqual(inventory['methodInfo'], "")
        self.assertEqual(inventory['attachments'], False)
        self.assertEqual(inventory['name'], "Matti Mattinen")
        self.assertEqual(inventory['email'], "matti@sposti.fi")
        self.assertEqual(inventory['phone'], "050556677")
        self.assertEqual(inventory['moreInfo'], "Ei ole..")
