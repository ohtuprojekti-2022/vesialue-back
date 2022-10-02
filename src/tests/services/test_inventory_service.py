import unittest
import pytest
import jwt
from utils.mongo import connect_to_db
from services.inventory_service import InventoryService
from werkzeug.exceptions import BadRequest
from utils.config import SECRET_KEY
import tests.test_tools as test_tools

BASE_URL = 'http://localhost:5000/api'
connect_to_db()

class TestInventoryService(unittest.TestCase):
    def setUp(self):
        test_tools.delete_all_inventories()
        self.ins = InventoryService()
    
    def test_add_inventory(self):
        inventory = self.ins.add_inventory({"coordinates":"N56.10.240 W03.22.260",
                                       "inventorydate":"2018-12-05",
                                       "method":"echo",
                                       "attachments":"True",
                                       "name":"Matti Mattinen",
                                       "email":"matti.mattinen@s-posti.fi",
                                       "phone":"0501234567",
                                       "more_info":"Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtaa kuvat ulkomuistista."})
        self.assertEqual(inventory, {
            "coordinates" : "N56.10.240 W03.22.260",
            "inventorydate" : "2018-12-05 00:00:00",
            "method" : "echo",
            "attachments" : "True",
            "name" : "Matti Mattinen",
            "email" : "matti.mattinen@s-posti.fi",
            "phone" : "0501234567",
            "more_info" : "Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtaa kuvat ulkomuistista."})
    '''
    def test_add_inventory_invalid_coordinates(self):
        with pytest.raises(BadRequest):
            self.ins.add_inventory({"coordinates":"N56.10240 W003.22.260",
                               "inventorydate":"2018-12-25 23:50:55.999",
                               "method":"echo",
                               "attachments":"True",
                               "name":"Matti Mattinen",
                               "email":"matti.mattinen@s-posti.fi",
                               "phone":"0501234567",
                               "more_info":"Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtaa kuvat ulkomuistista."
                               })
    '''    
    def test_add_inventory_invalid_date(self):
        with pytest.raises(BadRequest) as excinfo:
            self.ins.add_inventory({"coordinates":"N56.10.240 W003.22.260",
                               "inventorydate":"2018-1225",
                               "method":"echo",
                               "attachments":"True",
                               "name":"Matti Mattinen",
                               "email":"matti.mattinen@s-posti.fi",
                               "phone":"0501234567",
                               "more_info":"Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtaa kuvat ulkomuistista."
                               })
        self.assertEqual(str(excinfo.value), '400 Bad Request: Invalid date.')

    def test_add_inventory_invalid_method(self):
        with pytest.raises(BadRequest) as excinfo:
            self.ins.add_inventory({"coordinates":"N56.10.240 W003.22.260",
                               "inventorydate":"2018-12-25",
                               "method":"viisto",
                               "attachments":"True",
                               "name":"Matti Mattinen",
                               "email":"matti.mattinen@s-posti.fi",
                               "phone":"0501234567",
                               "more_info":"Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtaa kuvat ulkomuistista."
                               })
        self.assertEqual(str(excinfo.value), '400 Bad Request: Invalid method.')
        
    def test_add_inventory_invalid_email(self):
        with pytest.raises(BadRequest) as excinfo:
            self.ins.add_inventory({"coordinates":"N56.10.240 W003.22.260",
                               "inventorydate":"2018-12-25",
                               "method":"dive",
                               "attachments":"True",
                               "name":"Matti Mattinen",
                               "email":"matti.mattinen",
                               "phone":"0501234567",
                               "more_info":"Kamera katosi sukeltaessa, mutta voin tarvittaessa piirtaa kuvat ulkomuistista."
                               })
        self.assertEqual(str(excinfo.value), '400 Bad Request: Invalid email.')

    def test_create_multiple_users_with_valid_credentials(self):
        self.ins.add_inventory({"coordinates":"N26.10.240 E003.21.260",
                           "inventorydate":"2020-02-22",
                           "method":"dive",
                           "attachments":"False",
                           "name":"Maija Maijala",
                           "email":"hot_mail@hotmail.fi",
                           "phone":"0449996666",
                           "more_info":"Ei lisättävää."
                           })
        self.ins.add_inventory({"coordinates":"S16.10.940 E024.21.260",
                           "inventorydate":"2021-02-22",
                           "method":"sight",
                           "attachments":"False",
                           "name":"Anna Annala",
                           "email":"anna@hotmail.fi",
                           "phone":"09 111222333",
                           "more_info":"Hylyn näin, kun ohi kävelin."
                           })
        inventories = test_tools.get_all_inventories()
        self.assertEqual(len(list(inventories)), 2)
