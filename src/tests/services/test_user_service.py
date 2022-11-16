import unittest
import pytest
import jwt
from utils.mongo import connect_to_db
from services.user_service import user_service as us
from werkzeug.exceptions import BadRequest
from utils.config import SECRET_KEY
import tests.test_tools as test_tools
from models.user import User

BASE_URL = 'http://localhost:5000/api'
connect_to_db()

class TestUserService(unittest.TestCase):
    def setUp(self):
        test_tools.delete_all_users()
        self.user = User.create(username="testi",
                    password="12345678",
                    name="Sirpa Anneli",
                    email="elakelaiset@rymattyla.fi",
                    phone="09347787")
        self.user2 = User.create(username="mikko",
                    password="salainensana",
                    name="Mikko Mallikas",
                    email="postimaili@gmail.com",
                    phone="0507384955")

    def test_create_user_password_too_short(self):
        with pytest.raises(BadRequest):
            us.create_user({"username":"testilyhytsana",
                        "password":"lyhyt",
                        "name":"Lyhytsana Testaaja",
                        "email":"testiposti@gmail.com",
                        "phone":"0458384950"})

    def test_create_user_email_not_valid(self):
        with pytest.raises(BadRequest):
            us.create_user({"username":"spostitesti",
                        "password":"salainensana",
                        "name":"Posti Testaaja",
                        "email":"huonosposti",
                        "phone":"+358504332221"})

    def test_create_user_username_too_short(self):
        with pytest.raises(BadRequest):
            us.create_user({"username":"aa",
                        "password":"salainensana",
                        "name":"Lyhytnimi Testaaja",
                        "email":"testiposti@gmail.com",
                        "phone":"+358503445552"})

    def test_create_user_username_too_long(self):
        with pytest.raises(BadRequest):
            us.create_user({"username":"aivantajuttomanpitkäkäyttäjänimieihäntällaisiasaisiollakaan",
                        "password":"salainensalasana",
                        "name":"Pitkänimi Testaaja",
                        "email":"testiposti@gmail.com",
                        "phone":"0458380050"})

    def test_create_user_username_taken(self):
        us.create_user({"username":"taken_username",
                    "password":"salainensana",
                    "name":"Teppo Testaaja",
                    "email":"testiposti@gmail.com",
                    "phone":"+358407358893"})

        with pytest.raises(BadRequest):
            us.create_user({"username":"taken_username",
                        "password":"salainensana",
                        "name":"Teppo Testaaja",
                        "email":"testiposti@gmail.com",
                        "phone":"+358407358893"})

    def test_create_user_email_taken(self):
        us.create_user({"username":"emailtest2",
                    "password":"salainensana",
                    "name":"Teppo Testaaja",
                    "email":"emailtaken@gmail.com",
                    "phone":"+3584589990"})

        with pytest.raises(BadRequest):
            us.create_user({"username":"otheruser",
                        "password":"salainensana",
                        "name":"Teppo Testuser",
                        "email":"emailtaken@gmail.com",
                        "phone":"+3584589990"})

    def test_create_user_success(self):
        user = us.create_user({"username":"testaaja",
                "password":"salainensana",
                "name":"Teppo Testaaja",
                "email":"testiposti@gmail.com",
                "phone":"+358458594647"})

        self.assertEqual(user, {
            'id': str(user["id"]) or None,
            'name': "Teppo Testaaja",
            'email': "testiposti@gmail.com",
            'phone': "+358458594647",
            'username': "testaaja",
            'admin': "0"
            })
    
    def test_create_user_invalid_name(self):
        with pytest.raises(BadRequest):
            us.create_user({"username":"userperson500",
                        "password":"salainensana123",
                        "name":"abcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefg213455645764564555555555645645645643",
                        "email":"testimaili@gmail.com",
                        "phone":"0507485738"})

    def test_create_user_invalid_phone_number(self):
        with pytest.raises(BadRequest):
            us.create_user({"username":"userperson214",
                        "password":"salainensana",
                        "name":"Testi Testaaja",
                        "email":"testiposti@gmail.com",
                        "phone":"123"})

    def test_create_user_empty_phone_number(self):
        user = us.create_user({"username":"testaaja",
                "password":"salainensana",
                "name":"Teppo Testaaja",
                "email":"testiposti@gmail.com",
                "phone":""})

        self.assertEqual(user, {
            'id': str(user["id"]) or None,
            'name': "Teppo Testaaja",
            'email': "testiposti@gmail.com",
            'phone': "",
            'username': "testaaja",
            'admin': "0"
            })

    def test_create_multiple_users_with_valid_credentials(self):
        us.create_user({"username":"testaaja",
                "password":"salainensana",
                "name":"Teppo Testaaja",
                "email":"testiposti@gmail.com",
                "phone":"0508576839"})
        us.create_user({"username":"testaaja2",
                "password":"salainensana",
                "name":"Teppo Testaaja",
                "email":"testiposti2@gmail.com",
                "phone":"0508576839"})
        users = test_tools.get_all_users()
        self.assertEqual(len(list(users)), 4)

    def test_generate_token_generates_token(self):
        user = us.create_user({"username":"testaaja",
                "password":"salainensana",
                "name":"Teppo Testaaja",
                "email":"testiposti@gmail.com",
                "phone":"+358507338475"})

        token = us.generate_token(user)
        self.assertEqual(jwt.decode(token, SECRET_KEY, algorithms=["HS256"]), {'user_id': user['id'], 'admin': '0'})

    def test_login_invalid_credential_length(self):
        with pytest.raises(BadRequest):
            us.login_user("aa", "salainensana")

        with pytest.raises(BadRequest):
            us.login_user("testaaja", "aaaa")

        with pytest.raises(BadRequest):
            us.login_user("pitkäkäyttäjänimiehkäjopavähänliianpitkä", "salainensana")

        with pytest.raises(BadRequest):
            us.login_user("testaaja", "vmqdhbwjseawfyrpuzbdhlwefqmnijdyrqookiedlmmsfyamnlsdueyqpivjkyzlbeuekpbntoortiygyzjahmughhnlsdrnmmwbhruhcvchquatsdfratsqhftmyzakjm")

    def test_login_user_does_not_exist(self):
        with pytest.raises(BadRequest):
            us.login_user("olematon", "salainensana")

    def test_login_incorrect_password(self):
        us.create_user({"username":"testaaja",
            "password":"salainensana",
            "name":"Teppo Testaaja",
            "email":"testiposti@gmail.com",
            "phone":"+358452878939"})

        with pytest.raises(BadRequest):
            us.login_user("testaaja", "vääräsalasana")

    def test_login_correct_password(self):
        createduser = us.create_user({"username":"testaaja",
            "password":"salainensana",
            "name":"Teppo Testaaja",
            "email":"testiposti@gmail.com",
            "phone":"0407384950"})
        token = us.generate_token(createduser)

        loggeduser = us.login_user("testaaja", "salainensana")

        self.assertEqual(loggeduser, {"auth": token, "user": createduser})

    def test_set_admin(self):
        self.assertEqual(self.user.admin, 0)
        us.set_admin(self.user.username, 1)
        user = User.objects.raw({'username': {'$eq': self.user.username}}).first()
        self.assertEqual(user.admin, 1)

    def test_edit_user(self):
        user_json = self.user2.to_json()
        self.assertEqual(user_json, {
            'id': str(user_json["id"]) or None,
            'name': "Mikko Mallikas",
            'email': "postimaili@gmail.com",
            'phone': "0507384955",
            'username': "mikko",
            'admin': "0"
            })

        user_data = {'name': 'Mikko Mallikkaampi', 'phone': '044776655',
                     'email': 'mallikas_uusi@gmail.com', 'username': 'mikko'}
        us.edit(user_data)
        user = User.objects.raw({'username': {'$eq': self.user2.username}}).first()
        user_json2 = user.to_json()

        self.assertEqual(user_json2, {
            'id': str(user_json2["id"]) or None,
            'name': "Mikko Mallikkaampi",
            'email': "mallikas_uusi@gmail.com",
            'phone': "044776655",
            'username': "mikko",
            'admin': "0"
            })
