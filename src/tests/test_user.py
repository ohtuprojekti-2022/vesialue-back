import unittest
from utils.mongo import connect_to_db
from models.user import User
from werkzeug.security import check_password_hash

BASE_URL = 'http://localhost:5000/api'
connect_to_db()

class TestUser(unittest.TestCase):

    def test_create_user(self):
        user = User.create(username="testihenkilö",
                           password="salainensana",
                           name="Teppo Testaaja",
                           email="testiposti@gmail.com",
                           phone="1928374657")
        
        self.assertEqual(user.username, "testihenkilö")
        self.assertEqual(True, check_password_hash(user.password, "salainensana"))
        self.assertEqual(user.name, "Teppo Testaaja")
        self.assertEqual(user.email, "testiposti@gmail.com")
        self.assertEqual(user.phone, "1928374657")

    def test_to_json(self):
        user = User.create(username="testihenkilö",
                           password="salainensana",
                           name="Teppo Testaaja",
                           email="testiposti@gmail.com",
                           phone="1928374657")
       
        json = user.to_json()
        
        self.assertEqual(json, {
            'id': str(user._id) or None,
            'name': "Teppo Testaaja",
            'email': "testiposti@gmail.com",
            'phone': "1928374657",
            'username': "testihenkilö"
        })
