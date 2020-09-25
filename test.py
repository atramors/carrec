import unittest
import json
from unittest import mock
from carapp import app, db, db_models, endpoints

test_user = {
    "id": 100000,
    "username": "Ken1",
    "account_type": "client",
}


@mock.patch.object(endpoints, "User")
# Easier solution (check endpoints.py)
# @mock.patch("carapp.db_models.User")
class TestRequestMethods(unittest.TestCase):
    def test_get_user(self, MockUser):
        with app.test_client() as client:
            MockUser.query.get.return_value = test_user
            response = client.get("/user/100000")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()["id"], 100000)

    def test_get_user_failure(self, MockUser):
        with app.test_client() as client:
            MockUser.query.get.return_value = None
            response = client.get("/user/100000")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 404)

    def test_get_all_users(self, MockUser):
        with app.test_client() as client:
            MockUser.query.all.return_value = [
                test_user,
            ]
            response = client.get("/users")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json()[0], dict)
            self.assertEqual(response.status_code, 200)

    def test_get_all_users_failure(self, MockUser):
        with app.test_client() as client:
            MockUser.query.all.return_value = None
            response = client.get("/users")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 500)

    def test_post_user(self, MockUser):
        with app.test_client() as client:
            MockUser.return_value = test_user
            response = client.post("/user", json=test_user)
            self.assertIsNotNone(response)
            # self.assertIsInstance(response.get_json(), dict)
            # self.assertEqual(response.status_code, 201)

    def test_delete_user(self, MockUser):
        with app.test_client() as client:
            MockUser.query.get.return_value = test_user
            response = client.delete("/user/100000")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            # self.assertEqual(response.status_code, 204)
            # self.assertEqual(response.get_json(), {})

    def test_delete_user_failure(self, MockUser):
        with app.test_client() as client:
            MockUser.query.get.return_value = None
            response = client.delete("/user/100000")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(
                response.get_json(), {"Reason": "No User with such id here!"}
            )
