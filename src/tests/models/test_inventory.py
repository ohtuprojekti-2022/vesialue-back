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
                                     more_info="Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtaa kuvat ulkomuistista.")

        assert re.match(r'[0-9a-f]{24}', inventory.to_json()['areas'][0]['area'])
        self.assertEqual(inventory.user, self.user)
        self.assertEqual(inventory.inventorydate, datetime.datetime(1988, 3, 12, 0, 0))
        self.assertEqual(inventory.method, "dive")
        self.assertEqual(inventory.visibility, "normal")
        self.assertEqual(inventory.method_info, "")
        self.assertEqual(inventory.attachments, True)
        self.assertEqual(inventory.name, "")
        self.assertEqual(inventory.email, "")
        self.assertEqual(inventory.phone, "")
        self.assertEqual(
            inventory.more_info, "Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtaa kuvat ulkomuistista.")

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
                             more_info="Ei ole..")

        assert re.match(r'[0-9a-f]{24}', inventory.to_json()['areas'][0]['area'])
        self.assertEqual(inventory.user, None)
        self.assertEqual(inventory.inventorydate, datetime.datetime(1987, 3, 12, 0, 0))
        self.assertEqual(inventory.method, "dive")
        self.assertEqual(inventory.visibility, "normal")
        self.assertEqual(inventory.method_info, "")
        self.assertEqual(inventory.attachments, False)
        self.assertEqual(inventory.name, "Matti Mattinen")
        self.assertEqual(inventory.email, "matti@sposti.fi")
        self.assertEqual(inventory.phone, "050556677")
        self.assertEqual(inventory.more_info, "Ei ole..")

    def test_to_json(self):
        inventory = Inventory.create(COORDINATES,
        							 user=self.user,
        							 inventorydate="1966-03-12",
                                     method="dive",
                                     visibility="normal",
                                     method_info="",
                                     attachments=True,
                                     name="",
                                     email="",
                                     phone="",
                                     more_info="Vesi oli kylmää.")

        inventory_json = inventory.to_json()
        self.maxDiff=None
        self.assertEqual(inventory_json,
                         {'id': str(inventory._id),
                          'areas': [{
                              'area': inventory_json['areas'][0]['area']
                          }],
                          'attachments': True,
                          'inventorydate': '1966-03-12',
                          'method': 'dive',
                          'methodInfo': '',
                          'moreInfo' : 'Vesi oli kylmää.',
                          'name': '',
                          'email': '',
                          'phone': '',
                          'user': self.user.to_json(),
                          'visibility': 'normal'
        })
