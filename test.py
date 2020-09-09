import unittest
import carapp
from unittest import mock
from carapp import app, db, db_models, endpoints

@mock.patch("carapp.db_models.User")
class TestRequestMethods(unittest.TestCase):
    def test_get_all_users(self, MockUser):
        users = MockUser()
        users.get.return_value = [{"id": "666",
        "username": "admin",
        "password": "123456",
        "email": "admin_mail@test.com",
        "account_type": "client",
        },]
        response = users.get()
        self.assertIsNotNone(response)
        self.assertIsInstance(response[0], dict)
        self.assertEqual(response[0]["username"], "admin")
        

    # def test_get_all_users(self, user_id):
    #     return

