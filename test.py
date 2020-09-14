import unittest
import json
from unittest import mock
from carapp import app, db, db_models, endpoints


@mock.patch.object(endpoints, "User")
# Easier solution (check endpoints.py)
# @mock.patch("carapp.db_models.User")
class TestRequestMethods(unittest.TestCase):
    def test_get_user(self, MockUser):
        with app.test_client() as client:
            MockUser.query.get.return_value = {
                "id": 2,
                "email": "ane@nosat.com",
                "account_type": "client",
            }
            response = client.get("/user/2")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()["id"], 2)

    def test_get_user_failure(self, MockUser):
        with app.test_client() as client:
            MockUser.query.get.return_value = None
            response = client.get("/user/2")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 404)

    # def test_get_all_users(self, MockUser):
    #     with app.test_client() as client:
    #         test_users = MockUser()
    #         test_users.query.all.return_value = [
    #             {"id": 112, "email": "a1one@nosatana.com", "account_type": "client",},
    #         ]
    #         response = client.get("/users")
    #         self.assertIsNotNone(response)
    #         self.assertIsInstance(response.get_json()[0], dict)
    #         self.assertEqual(response.status_code, 200)
