from copy import deepcopy, copy
import unittest
import re
import pytest
import jwt
import json
from utils.mongo import connect_to_db
from services.inventory_service import InventoryService
from werkzeug.exceptions import BadRequest, NotFound
from tests.test_tools import COORDINATES_EDITED, TEST_REPORTS, USERS
import tests.test_tools as test_tools
from models.user import User

connect_to_db()


class TestInventoryService(unittest.TestCase):
    def setUp(self):
        test_tools.delete_all_inventories()
        test_tools.delete_all_users()
        test_tools.delete_all_edited_inventories()
        self.ins = InventoryService()
        self.user = User.create(username="testaaja",
                                password="sanasala123?",
                                name="Hanna Hannala",
                                email="hanna@sposti.fi",
                                phone="")

    def test_add_inventory(self):
        inventory = self.ins.add_inventory(TEST_REPORTS[0], None)[0]
        assert re.match(r'[0-9a-f]{24}', inventory['areas'][0]['area'])
        self.assertEqual(inventory['user'], None)
        self.assertEqual(inventory['inventorydate'][0:10], TEST_REPORTS[0]['inventorydate'])
        self.assertEqual(inventory['method'], TEST_REPORTS[0]['method'])
        self.assertEqual(inventory['attachments'], TEST_REPORTS[0]['attachments'])
        self.assertEqual(inventory['name'], TEST_REPORTS[0]['name'])
        self.assertEqual(inventory['email'], TEST_REPORTS[0]['email'])
        self.assertEqual(inventory['phone'], TEST_REPORTS[0]['phone'])
        self.assertEqual(inventory['moreInfo'], TEST_REPORTS[0]['moreInfo'])

    def test_add_inventory_with_user(self):
        inventory = self.ins.add_inventory(TEST_REPORTS[2], self.user)[0]
        assert re.match(r'[0-9a-f]{24}', inventory['areas'][0]['area'])
        self.assertEqual(inventory['user'], self.user.to_json())
        self.assertEqual(inventory['inventorydate'][0:10], TEST_REPORTS[2]['inventorydate'])
        self.assertEqual(inventory['method'], TEST_REPORTS[2]['method'])
        self.assertEqual(inventory['attachments'], TEST_REPORTS[2]['attachments'])
        self.assertEqual(inventory['name'], TEST_REPORTS[2]['name'])
        self.assertEqual(inventory['email'], TEST_REPORTS[2]['email'])
        self.assertEqual(inventory['phone'], TEST_REPORTS[2]['phone'])
        self.assertEqual(inventory['moreInfo'], TEST_REPORTS[2]['moreInfo'])

    def test_add_inventory_invalid_date(self):
        with pytest.raises(BadRequest) as excinfo:
            invalid_report = deepcopy(TEST_REPORTS[0])
            invalid_report['inventorydate'] = 'asdf'
            self.ins.add_inventory(invalid_report, None)
        self.assertEqual(str(excinfo.value), '400 Bad Request: Invalid date.')

    def test_add_inventory_invalid_method(self):
        with pytest.raises(BadRequest) as excinfo:
            invalid_report = deepcopy(TEST_REPORTS[0])
            invalid_report['method'] = 'asdf'
            self.ins.add_inventory(invalid_report, None)
        self.assertEqual(str(excinfo.value),
                         '400 Bad Request: Invalid method.')

    def test_add_inventory_invalid_coordinate_lng_too_big(self):
        invalid_report = deepcopy(TEST_REPORTS[0])
        with pytest.raises(BadRequest) as excinfo:
            coords = [[{"lat": 60.17797731341533, "lng": 181.903111488320214},
                       {"lat": 60.17473315099313, "lng": 24.886286597507773},
                       {"lat": 60.17114712497474, "lng": 24.899506154574706}]]
            invalid_report['areas'] = coords
            self.ins.add_inventory(invalid_report, None)
        self.assertEqual(str(excinfo.value), '400 Bad Request: Invalid areas.')

    def test_add_inventory_invalid_coordinate_lat_too_big(self):
        invalid_report = deepcopy(TEST_REPORTS[0])
        with pytest.raises(BadRequest) as excinfo:
            coords = [[{"lat": 60.17797731341533, "lng": 81.903111488320214},
                       {"lat": 60.17473315099313, "lng": 24.886286597507773},
                       {"lat": 80.17114712497474, "lng": 24.899506154574706}]]
            invalid_report['areas'] = coords
            self.ins.add_inventory(invalid_report, None)
        self.assertEqual(str(excinfo.value), '400 Bad Request: Invalid areas.')

    def test_add_inventory_invalid_coordinate_lat_invalid(self):
        invalid_report = deepcopy(TEST_REPORTS[0])
        with pytest.raises(BadRequest) as excinfo:
            coords = [[{"lat": 60.17797731341533, "lng": 81.903111488320214},
                       {"lot": 60, "lng": 24.886286597507773},
                       {"lat": 80.17114712497474, "lng": 24.899506154574706}]]
            invalid_report['areas'] = coords
            self.ins.add_inventory(invalid_report, None)
        self.assertEqual(str(excinfo.value), '400 Bad Request: Invalid areas.')

    def test_add_inventory_invalid_coordinate_not_list(self):
        invalid_report = deepcopy(TEST_REPORTS[0])
        with pytest.raises(BadRequest) as excinfo:
            coords = "'lat': '60.17797731341533', 'lng': '81.903111488320214'"
            invalid_report['areas'] = coords
            self.ins.add_inventory(invalid_report, None)
        self.assertEqual(str(excinfo.value), '400 Bad Request: Invalid areas.')

    def test_add_inventory_invalid_email(self):
        with pytest.raises(BadRequest) as excinfo:
            invalid_report = deepcopy(TEST_REPORTS[0])
            invalid_report['email'] = 'asdf'
            self.ins.add_inventory(invalid_report, None)
        self.assertEqual(str(excinfo.value), '400 Bad Request: Invalid email.')

    def test_add_inventory_invalid_phone(self):
        with pytest.raises(BadRequest) as excinfo:
            invalid_report = deepcopy(TEST_REPORTS[0])
            invalid_report['phone'] = 'numero'
            self.ins.add_inventory(invalid_report, None)
        self.assertEqual(str(excinfo.value), '400 Bad Request: Invalid phone number.')

    def test_create_multiple_inventory_reports_with_valid_info(self):
        self.ins.add_inventory(TEST_REPORTS[0], None)
        self.ins.add_inventory(TEST_REPORTS[1], None)
        inventories = test_tools.get_all_inventories()
        self.assertEqual(len(list(inventories)), 2)

    def test_get_inventory_by_id(self):
        id1 = self.ins.add_inventory(TEST_REPORTS[0], None)[0]['id']
        id2 = self.ins.add_inventory(TEST_REPORTS[1], None)[0]['id']

        inv1 = self.ins.get_inventory(id1)
        inv2 = self.ins.get_inventory(id2)

        inv1, inv2 = json.dumps(inv1, sort_keys=True), json.dumps(inv1, sort_keys=True)
        self.assertEqual(inv1, inv2)

    def test_get_inventory_invalid_id(self):
        self.ins.add_inventory(TEST_REPORTS[0], None)
        self.ins.add_inventory(TEST_REPORTS[1], None)
        with pytest.raises(NotFound) as excinfo:
            self.ins.get_inventory("asdf")
        self.assertEqual(str(excinfo.value), '404 Not Found: 404 not found')

    def test_get_areas_returns_empty_list_when_database_empty(self):
        areas = self.ins.get_areas()

        self.assertEqual(0, len(areas))

    def test_get_areas_returns_list_of_correct_length(self):
        self.ins.add_inventory(TEST_REPORTS[0], None)
        areas = self.ins.get_areas()
        self.assertEqual(1, len(areas))

    def test_get_all_inventories(self):
        self.ins.add_inventory(TEST_REPORTS[0], None)
        self.ins.add_inventory(TEST_REPORTS[1], None)
        inventories = self.ins.get_all_inventories()

        for inventory in inventories:
            inventory.pop("id")

        self.assertEqual(2, len(inventories))

    def test_get_all_inventories_returns_empty_list(self):
        inventories = self.ins.get_all_inventories()

        self.assertEqual(inventories, [])

    def test_add_edited_inventory_adds_valid_report_in_database(self):
        original_inventory = self.ins.add_inventory(TEST_REPORTS[2], self.user)[0]
        edited_report = copy(TEST_REPORTS[2])
        edited_report["areas"] = COORDINATES_EDITED
        edited_report["originalReport"] = original_inventory["id"]
        edited_inventory = self.ins.add_edited_inventory(edited_report, self.user)
        self.assertEqual(edited_inventory['areas'][0]['coordinates'], COORDINATES_EDITED[0])
        self.assertEqual(edited_inventory['user'], self.user.to_json())
        self.assertEqual(edited_inventory['inventorydate'][0:10], TEST_REPORTS[2]['inventorydate'])
        self.assertEqual(edited_inventory['method'], TEST_REPORTS[2]['method'])
        self.assertEqual(edited_inventory['attachments'], TEST_REPORTS[2]['attachments'])
        self.assertEqual(edited_inventory['name'], TEST_REPORTS[2]['name'])
        self.assertEqual(edited_inventory['email'], TEST_REPORTS[2]['email'])
        self.assertEqual(edited_inventory['phone'], TEST_REPORTS[2]['phone'])
        self.assertEqual(edited_inventory['moreInfo'], TEST_REPORTS[2]['moreInfo'])
        self.assertEqual(edited_inventory['originalReport'], original_inventory["id"])
    
    def test_add_edited_inventory_with_invalid_id_raises_exception(self):
        self.ins.add_inventory(TEST_REPORTS[2], self.user)[0]
        edited_report = copy(TEST_REPORTS[2])
        edited_report["areas"] = COORDINATES_EDITED
        edited_report["originalReport"] = "od3ef"
        
        with pytest.raises(BadRequest) as excinfo:
            self.ins.add_edited_inventory(edited_report, self.user)
        self.assertEqual(str(excinfo.value), '400 Bad Request: Invalid original report id.')

    def test_add_edited_inventory_with_incomplete_data_raises_exception(self):
        original_inventory = self.ins.add_inventory(TEST_REPORTS[2], self.user)[0]
        edited_report = copy(TEST_REPORTS[2])
        del edited_report["areas"]
        edited_report["originalReport"] = original_inventory["id"]
        with pytest.raises(BadRequest) as excinfo:
            self.ins.add_edited_inventory(edited_report, self.user)
        self.assertEqual(str(excinfo.value), '400 Bad Request: Invalid request, missing areas')

    def test_get_all_edited_inventories_returns_list_of_correct_size(self):
        original_inventory = self.ins.add_inventory(TEST_REPORTS[2], self.user)[0]
        edited_report = copy(TEST_REPORTS[2])
        edited_report["areas"] = COORDINATES_EDITED
        edited_report["originalReport"] = original_inventory["id"]
        self.ins.add_edited_inventory(edited_report, self.user)
        
        edited_inventories = self.ins.get_all_edited_inventories()
        self.assertEqual(1, len(edited_inventories))