import unittest
import datetime
from utils.mongo import connect_to_db
from models.inventory import Inventory
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

BASE_URL = 'http://localhost:5000/api'
connect_to_db()

class TestInventory(unittest.TestCase):

    def test_create_inventory(self):
        inventory = Inventory.create(coordinates="N56.10.240 W003.22.260",
                                     inventorydate="2018-12-25 23:50:55.999",
                                     method="kuvaus",
                                     attachments=True,
                                     name="Matti Mattinen",
                                     email="matti.mattinen@s-posti.fi",
                                     phone="0501234567",
                                     other="Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtaa kuvat ulkomuistista.")

        self.assertEqual(inventory.coordinates, "N56.10.240 W003.22.260")
        self.assertEqual(inventory.inventorydate, datetime.datetime(2018, 12, 25, 23, 50, 55, 999000))
        self.assertEqual(inventory.method, "kuvaus")
        self.assertEqual(inventory.attachments, True)
        self.assertEqual(inventory.name, "Matti Mattinen")
        self.assertEqual(inventory.email, "matti.mattinen@s-posti.fi")
        self.assertEqual(inventory.phone, "0501234567")
        self.assertEqual(inventory.other, "Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtaa kuvat ulkomuistista.")
