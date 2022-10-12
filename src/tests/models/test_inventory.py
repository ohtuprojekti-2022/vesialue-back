import unittest
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
        inventory = Inventory.create(areas=[],
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

        areas = []
        for area_coordinates in COORDINATES:
            areas.append(Area.create(inventory, area_coordinates))

        inventory = Inventory.update_areas(inventory, new_areas=areas)

        self.assertEqual(inventory.areas, areas)
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
        inventory = Inventory.create(areas=[],
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

        areas = []
        for area_coordinates in COORDINATES:
            areas.append(Area.create(inventory, area_coordinates))
        
        inventory = Inventory.update_areas(inventory, new_areas=areas)
        
        self.assertEqual(inventory.areas, areas)
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
        inventory = Inventory.create(areas=[],
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
        areas = []
        for area_coordinates in COORDINATES:
            areas.append(Area.create(inventory, area_coordinates))
        
        inventory = Inventory.update_areas(inventory, new_areas=areas)

        inventory_json = inventory.to_json()
        self.maxDiff=None
        self.assertEqual(inventory_json,
                         {'id': str(inventory._id),
                          'areas': [[{'lat': 60.17797731341533, 'lng': 1.903111488320214},
                                    {'lat': 60.17473315099313, 'lng': -24.886286597507773},
                                    {'lat': -70.17114712497474, 'lng': 24.899506154574706}]],
                          'user': self.user.to_json(),
                          'inventorydate': '1966-03-12 00:00:00',
                          'method': 'dive',
                          'attachments': True,
                          'name': '',
                          'email': '',
                          'phone': '',
                          'moreInfo' : 'Vesi oli kylmää.'
        })

