import unittest
import json
from unittest import mock
from carapp import app, db, db_models, endpoints


@mock.patch("carapp.db_models.User")
class TestRequestMethods(unittest.TestCase):
    def test_get_user(self, MockUser):
        with app.test_client() as client:
            test_user = MockUser()
            test_user.query.return_value = {
                "id": 112,
                "email": "a1one@nosatana.com",
                "account_type": "client",
            }
            response = client.get("/user/112")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()["id"], 112)

    def test_get_user_failure(self, MockUser):
        with app.test_client() as client:
            test_user = MockUser()
            test_user.query.return_value = {"Reason": "User not found", "user_id": 2}
            response = client.get("/user/2")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 404)

    # def test_get_all_users(self, user_id):
    #     return
