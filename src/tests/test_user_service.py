import unittest
import pytest
from utils.mongo import connect_to_db
from services.user_service import create_user, delete_all_users
from werkzeug.exceptions import BadRequest

BASE_URL = 'http://localhost:5000/api'
connect_to_db()

class TestUserService(unittest.TestCase):
    def setUp(self):
        delete_all_users()
    
    def test_create_user_password_too_short(self):
        with pytest.raises(BadRequest):
            create_user({"username":"testilyhytsana",
                        "password":"lyhyt",
                        "name":"Lyhytsana Testaaja",
                        "email":"testiposti@gmail.com",
                        "phone":"19283234677"})

    def test_create_user_email_not_valid(self):
        with pytest.raises(BadRequest):
            create_user({"username":"spostitesti",
                        "password":"salainensana",
                        "name":"Posti Testaaja",
                        "email":"huonosposti",
                        "phone":"102938475"})
    
    def test_create_user_username_too_short(self):
        with pytest.raises(BadRequest):
            create_user({"username":"aa",
                        "password":"salainensana",
                        "name":"Lyhytnimi Testaaja",
                        "email":"testiposti@gmail.com",
                        "phone":"32198700"})

    def test_create_user_username_taken(self):
        create_user({"username":"taken_username",
                    "password":"salainensana",
                    "name":"Teppo Testaaja",
                    "email":"testiposti@gmail.com",
                    "phone":"32198700"})
        
        with pytest.raises(BadRequest):
            create_user({"username":"taken_username",
                        "password":"salainensana",
                        "name":"Teppo Testaaja",
                        "email":"testiposti@gmail.com",
                        "phone":"32198700"})

    def test_create_user_success(self):
            user = create_user({"username":"testaaja",
                "password":"salainensana",
                "name":"Teppo Testaaja",
                "email":"testiposti@gmail.com",
                "phone":"32198700"})
            
            self.assertEqual(user, {
                'id': str(user["id"]) or None,
                'name': "Teppo Testaaja",
                'email': "testiposti@gmail.com",
                'phone': "32198700",
                'username': "testaaja"
                })
