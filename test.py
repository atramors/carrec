import unittest
import json
from unittest import mock
from carapp import app, db, db_models, endpoints


test_user = {
    "id": 100000,
    "username": "Kenn",
    "account_type": "client",
}


@mock.patch.object(endpoints, "User")
# Easier solution (check endpoints.py)
# @mock.patch("carapp.db_models.User")
class TestRequestMethods(unittest.TestCase):
    maxDiff = None

    def test_get_user(self, MockUser):
        with app.test_client() as client:
            MockUser.query.get.return_value = test_user
            response = client.get("/users/100000")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()["id"], 100000)

    def test_get_user_failure(self, MockUser):
        with app.test_client() as client:
            MockUser.query.get.return_value = None
            response = client.get("/users/100000")
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
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.get_json(), dict)
            self.assertIsInstance(response.get_json()["Users"][0], dict)
            self.assertEqual(response.get_json()["Users"][0], test_user)

    @mock.patch("carapp.db.session")
    def test_post_user(self, MockSession, MockUser):
        tester = {
            "id": 100000,
            "username": "Barbie",
            "password": "12134",
            "email": "Barbie@satana666.com",
            "account_type": "test-client",
        }
        with app.test_client() as client:
            MockUser.return_value = tester
            response = client.post("/users", json=tester)
            self.assertIsNotNone(response.get_json())
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.get_json(), tester)

    @mock.patch("carapp.db.session")
    def test_put_user(self, MockSession, MockUser):
        tester = {
            "id": 100000,
            "username": "Barbie",
            "password": "12134",
            "email": "Barbie@satana666.com",
            "account_type": "test-client",
        }
        with app.test_client() as client:
            MockUser.filter_by.update.return_value = tester
            response = client.put("/users/100000", json=tester)
            self.assertIsNotNone(response.get_json())
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), tester)

    @mock.patch("carapp.db.session")
    def test_delete_user(self, MockSession, MockUser):
        with app.test_client() as client:
            MockUser.query.get.return_value = test_user
            response = client.delete("/users/100000")
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 204)
            self.assertEqual(response.data, b"")

    def test_delete_user_failure(self, MockUser):
        with app.test_client() as client:
            MockUser.query.get.return_value = None
            response = client.delete("/users/100000")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.get_json(), {"Reason": "No User with id=100000"})
