import unittest
import datetime
from models.area import Area
from utils.mongo import connect_to_db
from models.inventory import Inventory
from tests.test_tools import COORDINATES

connect_to_db()


class TestInventory(unittest.TestCase):

    def test_create_inventory(self):
        inventory = Inventory.create(areas=[],
                                     inventorydate="2018-12-25 23:50:55.999",
                                     method="kuvaus",
                                     attachments=True,
                                     name="Matti Mattinen",
                                     email="matti.mattinen@s-posti.fi",
                                     phone="0501234567",
                                     more_info="Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtaa kuvat ulkomuistista.")

        areas = []
        for area_coordinates in COORDINATES:
            areas.append(Area.create(inventory, area_coordinates))

        inventory = Inventory.update_areas(inventory, new_areas=areas)

        self.assertEqual(inventory.areas, areas)
        self.assertEqual(inventory.inventorydate, datetime.datetime(
            2018, 12, 25, 23, 50, 55, 999000))
        self.assertEqual(inventory.method, "kuvaus")
        self.assertEqual(inventory.attachments, True)
        self.assertEqual(inventory.name, "Matti Mattinen")
        self.assertEqual(inventory.email, "matti.mattinen@s-posti.fi")
        self.assertEqual(inventory.phone, "0501234567")
        self.assertEqual(
            inventory.more_info, "Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtaa kuvat ulkomuistista.")
