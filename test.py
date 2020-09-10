import unittest
import carapp
import json
from marshmallow import Schema, fields
from unittest import mock
from carapp import app, db, db_models, endpoints


@mock.patch("carapp.db_models.User")
class TestRequestMethods(unittest.TestCase):
    def test_get_user(self, MockUser):
        with app.test_client() as client:

            test_user = MockUser()
            test_user.get.return_value = {
                "id": 112,
                "username": "lalanda1",
                "password": "12134",
                "email": "a1one@nosatana.com",
                "account_type": "client",
            }

            response = client.get("/user/112")

            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()["username"], "lalanda1")
            

    # def test_get_all_users(self, user_id):
    #     return

