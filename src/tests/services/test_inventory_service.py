from copy import deepcopy, copy
import unittest
import re
import pytest
import json
from services.inventory_service import InventoryService
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized
from werkzeug.security import generate_password_hash
from tests.test_tools import COORDINATES_EDITED, TEST_REPORTS
import tests.test_tools as test_tools
from models.user import User


class TestInventoryService(unittest.TestCase):
    def setUp(self):
        test_tools.delete_all_inventories()
        test_tools.delete_all_users()
        test_tools.delete_all_edited_inventories()
        test_tools.delete_all_delete_requests()
        self.ins = InventoryService()
        self.user = User.create(username="testaaja",
                                password_hash=generate_password_hash("sanasala123?"),
                                name="Hanna Hannala",
                                email="hanna@sposti.fi",
                                phone="")

    def test_add_inventory(self):
        inventory = self.ins.add_inventory(TEST_REPORTS[0], None, True)[0]
        assert re.match(r'[0-9a-f]{24}', inventory['areas'][0]['area'])
        self.assertEqual(inventory['user'], None)
        self.assertEqual(inventory['inventorydate']
                         [0:10], TEST_REPORTS[0]['inventorydate'])
        self.assertEqual(inventory['method'], TEST_REPORTS[0]['method'])
        self.assertEqual(inventory['attachments'],
                         TEST_REPORTS[0]['attachments'])
        self.assertEqual(inventory['name'], TEST_REPORTS[0]['name'])
        self.assertEqual(inventory['email'], TEST_REPORTS[0]['email'])
        self.assertEqual(inventory['phone'], TEST_REPORTS[0]['phone'])
        self.assertEqual(inventory['moreInfo'], TEST_REPORTS[0]['moreInfo'])

    def test_add_inventory_with_user(self):
        inventory = self.ins.add_inventory(TEST_REPORTS[2], self.user, True)[0]
        assert re.match(r'[0-9a-f]{24}', inventory['areas'][0]['area'])
        self.assertEqual(inventory['user'], self.user.to_json())
        self.assertEqual(inventory['inventorydate']
                         [0:10], TEST_REPORTS[2]['inventorydate'])
        self.assertEqual(inventory['method'], TEST_REPORTS[2]['method'])
        self.assertEqual(inventory['attachments'],
                         TEST_REPORTS[2]['attachments'])
        self.assertEqual(inventory['name'], TEST_REPORTS[2]['name'])
        self.assertEqual(inventory['email'], TEST_REPORTS[2]['email'])
        self.assertEqual(inventory['phone'], TEST_REPORTS[2]['phone'])
        self.assertEqual(inventory['moreInfo'], TEST_REPORTS[2]['moreInfo'])

    def test_add_inventory_invalid_date_format(self):
        with pytest.raises(BadRequest) as excinfo:
            invalid_report = deepcopy(TEST_REPORTS[0])
            invalid_report['inventorydate'] = 'asdf'
            self.ins.add_inventory(invalid_report, None)
        self.assertEqual(str(excinfo.value), '400 Bad Request: Invalid date.')

    def test_add_inventory_invalid_date_date(self):
        with pytest.raises(BadRequest) as excinfo:
            invalid_report = deepcopy(TEST_REPORTS[0])
            invalid_report['inventorydate'] = '3000-01-01'
            self.ins.add_inventory(invalid_report, None)
        self.assertEqual(str(excinfo.value),
                         '400 Bad Request: Date cannot be in the future.')

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
            invalid_report['phone'] = '112'
            self.ins.add_inventory(invalid_report, None)
        self.assertEqual(str(excinfo.value),
                         '400 Bad Request: Invalid phone number.')

    def test_add_inventory_invalid_method_info(self):
        with pytest.raises(BadRequest) as excinfo:
            invalid_report = deepcopy(TEST_REPORTS[0])
            invalid_report['methodInfo'] = 'Tein inventoinnin sellaisella tavalla ett?? menin sukeltamaan veteen ilman mit????n v??lineit?? ja yritin painaa mieleeni mit?? vedess?? n??in.'
            self.ins.add_inventory(invalid_report, None)
        self.assertEqual(str(excinfo.value),
                         '400 Bad Request: Method info too long.')

        with pytest.raises(BadRequest) as excinfo:
            invalid_report = deepcopy(TEST_REPORTS[0])
            invalid_report['methodInfo'] = ''
            self.ins.add_inventory(invalid_report, None)
        self.assertEqual(str(excinfo.value),
                         '400 Bad Request: No method info given.')

    def test_add_inventory_with_too_long_description(self):
        with pytest.raises(BadRequest) as excinfo:
            invalid_report = deepcopy(TEST_REPORTS[0])
            invalid_report['moreInfo'] = 'a' * 5001
            self.ins.add_inventory(invalid_report, None)
        self.assertEqual(str(excinfo.value), '400 Bad Request: Info too long.')

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

        inv1, inv2 = json.dumps(inv1, sort_keys=True), json.dumps(
            inv1, sort_keys=True)
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
        original_inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        edited_report = copy(TEST_REPORTS[2])
        edited_report["areas"] = COORDINATES_EDITED
        edited_report["editReason"] = "test reason"
        edited_report["originalReport"] = original_inventory["id"]
        del (edited_report["name"])
        del (edited_report["email"])
        del (edited_report["phone"])
        edited_inventory = self.ins.add_edited_inventory(
            edited_report, self.user)
        self.assertEqual(
            edited_inventory['areas'][0]['coordinates'], COORDINATES_EDITED[0])
        self.assertEqual(edited_inventory['user'], self.user.to_json())
        self.assertEqual(
            edited_inventory['inventorydate'][0:10], TEST_REPORTS[2]['inventorydate'])
        self.assertEqual(edited_inventory['method'], TEST_REPORTS[2]['method'])
        self.assertEqual(
            edited_inventory['attachments'], TEST_REPORTS[2]['attachments'])
        self.assertEqual(
            edited_inventory['moreInfo'], TEST_REPORTS[2]['moreInfo'])
        self.assertEqual(
            edited_inventory['originalReport'], original_inventory["id"])

    def test_add_edited_inventory_with_invalid_id_raises_exception(self):
        self.ins.add_inventory(TEST_REPORTS[2], self.user)[0]
        edited_report = copy(TEST_REPORTS[2])
        edited_report["areas"] = COORDINATES_EDITED
        edited_report["editReason"] = "test reason"
        edited_report["originalReport"] = "od3ef"

        with pytest.raises(BadRequest) as excinfo:
            self.ins.add_edited_inventory(edited_report, self.user)
        self.assertEqual(str(excinfo.value),
                         '400 Bad Request: Invalid original report id.')

    def test_add_edited_inventory_with_incomplete_data_raises_exception(self):
        original_inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        edited_report = copy(TEST_REPORTS[2])
        del edited_report["areas"]
        edited_report["editReason"] = "test reason"
        edited_report["originalReport"] = original_inventory["id"]

        with pytest.raises(BadRequest) as excinfo:
            self.ins.add_edited_inventory(edited_report, self.user)
        self.assertEqual(str(excinfo.value),
                         '400 Bad Request: Invalid request, missing areas')

    def test_get_all_edited_inventories_returns_list_of_correct_size(self):
        original_inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        edited_report = copy(TEST_REPORTS[2])
        edited_report["areas"] = COORDINATES_EDITED
        edited_report["editReason"] = "test reason"
        edited_report["originalReport"] = original_inventory["id"]
        self.ins.add_edited_inventory(edited_report, self.user)

        edited_inventories = self.ins.get_all_edited_inventories(True)
        self.assertEqual(1, len(edited_inventories))

    def test_get_all_edited_inventories_as_non_admin_results_in_exception(self):
        with pytest.raises(Unauthorized) as excinfo:
            self.ins.get_all_edited_inventories(False)
        self.assertEqual(str(excinfo.value), '401 Unauthorized: Admin only')

    def test_get_edited_inventory_invalid_id(self):
        original_inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        edited_report = copy(TEST_REPORTS[2])
        edited_report["areas"] = COORDINATES_EDITED
        edited_report["editReason"] = "test reason"
        edited_report["originalReport"] = original_inventory["id"]
        self.ins.add_edited_inventory(edited_report, self.user)

        with pytest.raises(NotFound) as excinfo:
            self.ins.get_edited_inventory("asdf", True)
        self.assertEqual(str(excinfo.value), '404 Not Found: 404 not found')

    def test_get_edited_inventory_valid_id(self):
        original_inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        edited_report = copy(TEST_REPORTS[2])
        edited_report["areas"] = COORDINATES_EDITED
        edited_report["editReason"] = "test reason"
        edited_report["originalReport"] = original_inventory["id"]
        edited_inventory = self.ins.add_edited_inventory(
            edited_report, self.user)

        inv_id = edited_inventory['id']

        search = self.ins.get_edited_inventory(inv_id, True)
        self.assertEqual(search, edited_inventory)

    def test_get_edited_inventory_as_non_admin_raises_exception(self):
        original_inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        edited_report = copy(TEST_REPORTS[2])
        edited_report["areas"] = COORDINATES_EDITED
        edited_report["editReason"] = "test reason"
        edited_report["originalReport"] = original_inventory["id"]
        edited_inventory = self.ins.add_edited_inventory(
            edited_report, self.user)

        inv_id = edited_inventory['id']
        with pytest.raises(Unauthorized) as excinfo:
            self.ins.get_edited_inventory(inv_id, False)
        self.assertEqual(str(excinfo.value), '401 Unauthorized: Admin only')

    def test_approving_edited_inventory_changes_the_original(self):
        original_inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        edited_report = copy(TEST_REPORTS[2])
        edited_report["areas"] = COORDINATES_EDITED
        edited_report["editReason"] = "test reason"
        edited_report["originalReport"] = original_inventory["id"]
        edited_inventory = self.ins.add_edited_inventory(
            edited_report, self.user)
        inv_id = edited_inventory['id']
        self.ins.approve_edit(inv_id, True)

        original_inv_changed = self.ins.get_inventory(original_inventory["id"])
        self.assertNotEqual(
            original_inventory["areas"], original_inv_changed["areas"])

    def test_non_admin_approval_results_in_exception(self):
        original_inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        edited_report = copy(TEST_REPORTS[2])
        edited_report["areas"] = COORDINATES_EDITED
        edited_report["editReason"] = "test reason"
        edited_report["originalReport"] = original_inventory["id"]
        edited_inventory = self.ins.add_edited_inventory(
            edited_report, self.user)
        inv_id = edited_inventory['id']
        with pytest.raises(Unauthorized) as excinfo:
            self.ins.approve_edit(inv_id)
        self.assertEqual(str(excinfo.value), '401 Unauthorized: Admin only')

    def test_delete_edit_deletes_from_database(self):
        original_inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        edited_report = copy(TEST_REPORTS[2])
        edited_report["areas"] = COORDINATES_EDITED
        edited_report["editReason"] = "test reason"
        edited_report["originalReport"] = original_inventory["id"]
        edited_inventory = self.ins.add_edited_inventory(
            edited_report, self.user)
        inv_id = edited_inventory['id']
        self.ins.delete_edit(inv_id, True)

        with pytest.raises(NotFound) as excinfo:
            self.ins.get_edited_inventory(inv_id, True)
        self.assertEqual(str(excinfo.value), '404 Not Found: 404 not found')

    def test_deleting_own_edit_request_without_admin_status_should_succeed(self):
        original_inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        edited_report = copy(TEST_REPORTS[2])
        edited_report["areas"] = COORDINATES_EDITED
        edited_report["editReason"] = "test reason"
        edited_report["originalReport"] = original_inventory["id"]
        edited_inventory = self.ins.add_edited_inventory(
            edited_report, self.user)
        inv_id = edited_inventory['id']
        self.ins.delete_edit(inv_id, is_admin=False, user_id=self.user._id)

        with pytest.raises(NotFound) as excinfo:
            self.ins.get_edited_inventory(inv_id, True)
        self.assertEqual(str(excinfo.value), '404 Not Found: 404 not found')

    def test_delete_edit_raises_exception_when_given_invalid_id(self):
        with pytest.raises(NotFound) as excinfo:
            self.ins.delete_edit('4328gh', True)
        self.assertEqual(str(excinfo.value), '404 Not Found: 404 not found')

    def test_unauthorized_delete_edit_raises_exception(self):
        original_inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        edited_report = copy(TEST_REPORTS[2])
        edited_report["areas"] = COORDINATES_EDITED
        edited_report["editReason"] = "test reason"
        edited_report["originalReport"] = original_inventory["id"]
        edited_inventory = self.ins.add_edited_inventory(
            edited_report, self.user)
        inv_id = edited_inventory['id']

        with pytest.raises(Unauthorized) as excinfo:
            self.ins.delete_edit(inv_id, False)
        self.assertEqual(str(excinfo.value), '401 Unauthorized: Admin only')

    def test_adding_edited_inventory_with_different_user_results_in_exception(self):
        user_b = User.create(username="mephisto",
                             password_hash=generate_password_hash(
                                 "abrakadabra62"),
                             name="Mephistopheles",
                             email="mephisto@sposti.fi",
                             phone="")
        original_inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        edited_report = copy(TEST_REPORTS[2])
        edited_report["areas"] = COORDINATES_EDITED
        edited_report["editReason"] = "test reason"
        edited_report["originalReport"] = original_inventory["id"]
        with pytest.raises(Unauthorized) as excinfo:
            self.ins.add_edited_inventory(edited_report, user_b)
        self.assertEqual(str(excinfo.value),
                         '401 Unauthorized: Authorization error')

    def test_delete_inventory_as_admin_is_successful(self):
        inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        self.ins.delete_inventory(inventory["id"], True)

        with pytest.raises(NotFound) as excinfo:
            self.ins.get_inventory(inventory["id"], True)
        self.assertEqual(str(excinfo.value), '404 Not Found: 404 not found')

    def test_delete_inventory_as_non_admin_raises_exception(self):
        inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        with pytest.raises(Unauthorized) as excinfo:
            self.ins.delete_inventory(inventory["id"], False)
        self.assertEqual(str(excinfo.value),
                         '401 Unauthorized: Admin only')
        search = self.ins.get_inventory(inventory["id"])
        self.assertEqual(search, inventory)

    def test_delete_inventory_ivanlid_id_raises_exception(self):
        with pytest.raises(NotFound) as excinfo:
            self.ins.delete_inventory('asdf', True)
        self.assertEqual(str(excinfo.value), '404 Not Found: 404 not found')

    def test_successful_delete_request_returns_json(self):
        inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        data = {'inventory': inventory['id'],
                'reason': 'tein vahingossa kopion'}
        
        result = self.ins.request_deletion(data, self.user)

        self.assertIsNotNone(result['id'])
        self.assertEqual(result['inventory'], data['inventory'])
        self.assertEqual(result['reason'], data['reason'])
    
    def test_request_deletion_by_different_user_results_in_exception(self):
        other_user = User.create(username="mephisto",
                             password_hash=generate_password_hash("abrakadabra62"),
                             name="Mephistopheles",
                             email="mephisto@sposti.fi",
                             phone="")

        inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        data = {'inventory': inventory['id'],
                'reason': 'en pid?? t??st??'}
        with pytest.raises(Unauthorized) as excinfo:
            self.ins.request_deletion(data, other_user)
        self.assertEqual(str(excinfo.value),
                         '401 Unauthorized: Authorization error')

    def test_approve_deletion_with_invalid_id_results_in_exception(self):
        with pytest.raises(NotFound) as excinfo:
            self.ins.approve_deletion('fde24d', True)
        self.assertEqual(str(excinfo.value),
                         '404 Not Found: 404 not found')

    def test_approve_deletion_as_non_admin_results_in_exception(self):
        inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        data = {'inventory': inventory['id'],
                'reason': 'tein vahingossa kopion'}
        
        result = self.ins.request_deletion(data, self.user)
        with pytest.raises(Unauthorized) as excinfo:
            self.ins.approve_deletion(result['id'], False)
        self.assertEqual(str(excinfo.value),
                         '401 Unauthorized: Admin only')
        requests = self.ins.get_all_delete_requests(True)
        self.assertEqual(1, len(requests))
    
    def test_approve_deletion_as_admin_successfully_removes_request_and_inventory(self):
        inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        data = {'inventory': inventory['id'],
                'reason': 'tein vahingossa kopion'}
        
        result = self.ins.request_deletion(data, self.user)
        self.ins.approve_deletion(result['id'], True)
        
        requests = self.ins.get_all_delete_requests(True)
        self.assertEqual(0, len(requests))
        with pytest.raises(NotFound) as excinfo:
            self.ins.get_inventory(result['inventory'])
        self.assertEqual(str(excinfo.value),
                         '404 Not Found: 404 not found')
    
    def test_removing_delete_requests_as_non_admin_results_in_exception(self):
        inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        data = {'inventory': inventory['id'],
                'reason': 'tein vahingossa kopion'}
        
        result = self.ins.request_deletion(data, self.user)
        with pytest.raises(Unauthorized) as excinfo:
            self.ins.remove_delete_request(result['id'], False, user_id='1b2h3647jd83kd9g')
        self.assertEqual(str(excinfo.value),
                         '401 Unauthorized: Admin only')
        requests = self.ins.get_all_delete_requests(True)
        self.assertEqual(1, len(requests))
    
    def test_removing_delete_request_with_invalid_id_results_in_exception(self):
        with pytest.raises(NotFound) as excinfo:
            self.ins.remove_delete_request('fde24d', True, None)
        self.assertEqual(str(excinfo.value),
                         '404 Not Found: 404 not found')
    
    def test_removing_delete_request_with_valid_id_and_admin_status_succesful(self):
        inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        data = {'inventory': inventory['id'],
                'reason': 'tein vahingossa kopion'}

        result = self.ins.request_deletion(data, self.user)
        self.ins.remove_delete_request(result['id'], True, None)

        requests = self.ins.get_all_delete_requests(True)
        self.assertEqual(0, len(requests))
        inventory = self.ins.get_inventory(result['inventory'])
        self.assertIsNotNone(inventory)

    def test_removing_own_delete_request_without_admin_status_should_succeed(self):
        inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        data = {'inventory': inventory['id'],
                'reason': 'tein vahingossa kopion'}

        result = self.ins.request_deletion(data, self.user)
        self.ins.remove_delete_request(result['id'], False, self.user._id)

        requests = self.ins.get_all_delete_requests(True)
        self.assertEqual(0, len(requests))
        inventory = self.ins.get_inventory(result['inventory'])
        self.assertIsNotNone(inventory)

    def test_get_all_delete_requests_as_non_admin_results_in_excpetion(self):
        with pytest.raises(Unauthorized) as excinfo:
            self.ins.get_all_delete_requests(False)
        self.assertEqual(str(excinfo.value),
                         '401 Unauthorized: Admin only')

    def test_get_all_delete_requests_successful_as_admin(self):
        inventory = self.ins.add_inventory(
            TEST_REPORTS[2], self.user)[0]
        data = {'inventory': inventory['id'],
                'reason': 'tein vahingossa kopion'}

        self.ins.request_deletion(data, self.user)
        result = self.ins.get_all_delete_requests(True)
        self.assertEqual(1, len(result))
