import unittest
from entities import inventory

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = inventory.Inventory(name="Matti Mattinen",
        			email="matti.mattinen@s-posti.fi",
        			phonenumber="0501234567",
        			other="Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtaa kuvat ulkomuistista.")

    def test_create_inventory(self):
        self.assertEqual(self.inventory.get_name(), "Matti Mattinen")
        self.assertEqual(self.inventory.get_email(), "matti.mattinen@s-posti.fi")
        self.assertEqual(self.inventory.get_phonenumber(), "0501234567")
        self.assertEqual(self.inventory.get_other(), "Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtaa kuvat ulkomuistista.")

    def test_set_name(self):
        self.inventory.set_name("Anna Annala")
        self.assertEqual(self.inventory.get_name(), "Anna Annala")

    def test_set_email(self):
        self.inventory.set_email("postiluukku@luukku.com")
        self.assertEqual(self.inventory.get_email(), "postiluukku@luukku.com")

    def test_set_phonenumber(self):
        self.inventory.set_phonenumber("020304")
        self.assertEqual(self.inventory.get_phonenumber(), "020304")

    def test_set_other(self):
        self.inventory.set_other("Ei muuta")
        self.assertEqual(self.inventory.get_other(), "Ei muuta")

