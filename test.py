import unittest
import json
from unittest import mock
from carapp import app, db, db_models, endpoints


@mock.patch("db_models.User")
class TestRequestMethods(unittest.TestCase):
    def test_get_user(self, MockUser):
        with app.test_client() as client:
            t_user = MockUser.return_value
            # db_models.User() = {
            t_user["id"] = 2
            t_user["email"] = "ane@nosatana.com"
            t_user["account_type"] = "client"
            t_user["username"] = "Ken2"
            t_user["password"] = "12134"
            # }
            # MockUser = MockUser()
            MockUser.query.get({
                "id": 2,
                "email": "ane@nosatana.com",
                "account_type": "client",
            }).return_value = t_user
            response = client.get("/user/2")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()["id"], 2)
        # test_user = db_models.User()
        # test_user.id = 2
        # test_user.email = 'a1one@nosatana.com'
        # MockUser.query.get.return_value = [test_user]
        # response = endpoints.UserData.get(self, user_id)
        # import pdb; pdb.set_trace()
        # self.assertIsNotNone(response)
        # self.assertIsInstance(response.get_json(), dict)
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.get_json()["id"], 2)

    # def test_get_user_failure(self, MockUser):
    #     with app.test_client() as client:
    #         test_user = MockUser()
    #         test_user.query.get.return_value = {}
    #         response = client.get("/user/2")
    #         self.assertIsNotNone(response)
    #         self.assertIsInstance(response.get_json(), dict)
    #         self.assertEqual(response.status_code, 404)

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
