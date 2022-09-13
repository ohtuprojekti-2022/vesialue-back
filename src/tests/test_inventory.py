import unittest
from entities import inventory

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = inventory.Inventory(name="Matti Mattinen",
        			email="matti.mattinen@s-posti.fi",
        			phonenumber="0501234567",
                    coordinates="N56°10.240 W003°22.260",
                    time="eilen",
                    methods="kuvaus",
                    attachments=True,
        			other="Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtaa kuvat ulkomuistista.")

    def test_create_inventory(self):
        self.assertEqual(self.inventory.get_name(), "Matti Mattinen")
        self.assertEqual(self.inventory.get_email(), "matti.mattinen@s-posti.fi")
        self.assertEqual(self.inventory.get_phonenumber(), "0501234567")
        self.assertEqual(self.inventory.get_coordinates(), "N56°10.240 W003°22.260")
        self.assertEqual(self.inventory.get_time(), "eilen")
        self.assertEqual(self.inventory.get_methods(), "kuvaus")
        self.assertEqual(self.inventory.get_attachments(), True)
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

    def test_set_coordinates(self):
        self.inventory.set_coordinates("S56°10.240 E003°22.260")
        self.assertEqual(self.inventory.get_coordinates(), "S56°10.240 E003°22.260")

    def test_set_time(self):
        self.inventory.set_time("020304")
        self.assertEqual(self.inventory.get_time(), "020304")

    def test_set_methods(self):
        self.inventory.set_methods("toinen")
        self.assertEqual(self.inventory.get_methods(), "toinen")

    def test_set_attachments(self):
        self.inventory.set_attachments(False)
        self.assertEqual(self.inventory.get_attachments(), False)

    def test_set_other(self):
        self.inventory.set_other("Ei muuta")
        self.assertEqual(self.inventory.get_other(), "Ei muuta")

