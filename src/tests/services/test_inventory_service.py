from copy import deepcopy
import unittest
import pytest
import jwt
from utils.mongo import connect_to_db
from services.inventory_service import InventoryService
from werkzeug.exceptions import BadRequest
from tests.test_tools import TEST_REPORTS
import tests.test_tools as test_tools

connect_to_db()


class TestInventoryService(unittest.TestCase):
    def setUp(self):
        test_tools.delete_all_inventories()
        self.ins = InventoryService()


    def test_add_inventory(self):
        inventory = self.ins.add_inventory(TEST_REPORTS[0])
        self.assertEqual(inventory['areas'], TEST_REPORTS[0]['coordinates'])
        self.assertEqual(inventory['inventorydate'][0:10], TEST_REPORTS[0]['inventorydate'])
        self.assertEqual(inventory['method'], TEST_REPORTS[0]['method'])
        self.assertEqual(inventory['attachments'], TEST_REPORTS[0]['attachments'])
        self.assertEqual(inventory['name'], TEST_REPORTS[0]['name'])
        self.assertEqual(inventory['email'], TEST_REPORTS[0]['email'])
        self.assertEqual(inventory['phone'], TEST_REPORTS[0]['phone'])
        self.assertEqual(inventory['moreInfo'], TEST_REPORTS[0]['moreInfo'])

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
            invalid_report = deepcopy(TEST_REPORTS[0])
            invalid_report['inventorydate'] = 'asdf'
            self.ins.add_inventory(invalid_report)
        self.assertEqual(str(excinfo.value), '400 Bad Request: Invalid date.')


    def test_add_inventory_invalid_method(self):
        with pytest.raises(BadRequest) as excinfo:
            invalid_report = deepcopy(TEST_REPORTS[0])
            invalid_report['method'] = 'asdf'
            self.ins.add_inventory(invalid_report)
        self.assertEqual(str(excinfo.value),
                         '400 Bad Request: Invalid method.')


    def test_add_inventory_invalid_email(self):
        with pytest.raises(BadRequest) as excinfo:
            invalid_report = deepcopy(TEST_REPORTS[0])
            invalid_report['email'] = 'asdf'
            self.ins.add_inventory(invalid_report)
        self.assertEqual(str(excinfo.value), '400 Bad Request: Invalid email.')


    def test_create_multiple_inventory_reports_with_valid_info(self):
        self.ins.add_inventory(TEST_REPORTS[0])
        self.ins.add_inventory(TEST_REPORTS[1])
        inventories = test_tools.get_all_inventories()
        self.assertEqual(len(list(inventories)), 2)
