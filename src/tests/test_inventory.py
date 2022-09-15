import unittest
import datetime
from models.inventory import Inventory

class TestInventory(unittest.TestCase):

    def test_create_inventory(self):
        inventory = Inventory.create(coordinates="N56°10.240 W003°22.260",
                                     time=datetime.datetime.now(),
                                     methods="kuvaus",
                                     attachments=True,
                                     name="Matti Mattinen",
                                     email="matti.mattinen@s-posti.fi",
                                     phonenumber="0501234567",
                                     other="Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtaa kuvat ulkomuistista.")

        self.assertEqual(inventory.coordinates, "N56°10.240 W003°22.260")
        self.assertEqual(inventory.time, datetime.datetime.now())
        self.assertEqual(inventory.methods, "kuvaus")
        self.assertEqual(inventory.attachments, True)
        self.assertEqual(inventory.name, "Matti Mattinen")
        self.assertEqual(inventory.email, "matti.mattinen@s-posti.fi")
        self.assertEqual(inventory.phonenumber, "0501234567")
        self.assertEqual(inventory.other, "Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtaa kuvat ulkomuistista.")
