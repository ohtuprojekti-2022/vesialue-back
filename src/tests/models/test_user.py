import unittest
from tests.test_tools import delete_all_users
from utils.mongo import connect_to_db
from models.user import User
from werkzeug.security import check_password_hash

BASE_URL = 'http://localhost:5000/api'
connect_to_db()

class TestUser(unittest.TestCase):
    def setUp(self):
        delete_all_users()
        self.user = User.create(username="testihenkilö",
                    password="salainensana",
                    name="Teppo Testaaja",
                    email="testiposti@gmail.com",
                    phone="1928374657")

    def test_create_user(self):
        self.assertEqual(self.user.username, "testihenkilö")
        self.assertEqual(True, check_password_hash(self.user.password, "salainensana"))
        self.assertEqual(self.user.name, "Teppo Testaaja")
        self.assertEqual(self.user.email, "testiposti@gmail.com")
        self.assertEqual(self.user.phone, "1928374657")

    def test_to_json(self):
        json = self.user.to_json()
        
        self.assertEqual(json, {
            'id': str(self.user._id) or None,
            'name': "Teppo Testaaja",
            'email': "testiposti@gmail.com",
            'phone': "1928374657",
            'username': "testihenkilö"
        })
