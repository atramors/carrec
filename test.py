import unittest
from unittest import mock

from carapp import app

TESTER = {
    "id": 100000,
    "username": "Barbie",
    "password": "12134",
    "email": "Barbie@satana666.com",
    "account_type": "test-client",
}
TEST_USER = {
    "id": 100000,
    "username": "Kenn",
    "account_type": "client",
}
TEST_CAR = {
    "id": 100000,
    "car_title": "Supercar",
    "title": "Supercar 3000",
    "condition": "New",
    "body_type": "Sedan",
    "brand": "Supercar",
    "model": "Car",
    "year_of_production": "3000",
    "country_origin": "Supercountry",
    "country_now": "Supercountry",
    "city": "Supercity",
    "mileage": "0 km",
    "technical_condition": "Supercondition",
    "gear_box": "Manual",
    "fuel_type": "Gasoline",
    "engine": "10 l (666 hp / 100 kW)",
    "color": "White",
    "safety": "Supersafe",
    "wanted": "No",
    "multimedia": "Subwoofer",
    "comfort": "Supercomfort",
    "picture": "Cool pic",
    "price": "1000000$",
    "warranty": "12 months",
    "fuel_consumption": "2l/100km",
    "drivetrain": "4matic",
    "user_id": 999,
}


class TestRequestMethods(unittest.TestCase):
    maxDiff = None

    @mock.patch("carapp.db_models.User")
    @mock.patch("carapp.db.session")
    def test_signup_user(self, mock_session, mock_user):
        with app.test_client() as client:
            mock_user.return_value = TESTER
            response = client.post("/signup", json=TESTER)
            self.assertIsNotNone(response.get_json())
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.get_json(), TESTER)

    @unittest.skip('wip')
    # @mock.patch("carapp.authent.user_loader")
    @mock.patch("carapp.db_models.User")
    def test_get_user(self, mock_user):  # , MockToken):
        with app.test_client() as client:
            # MockToken.return_value = True
            mock_user.query.get.return_value = TEST_USER
            response = client.get("/user/100000")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()["id"], 100000)

    @unittest.skip("wip")
    @mock.patch("carapp.db_models.User")
    def test_get_user_failure(self, mock_user):
        with app.test_client() as client:
            mock_user.query.get.return_value = None
            response = client.get("/user/100000")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 404)

    @unittest.skip("wip")
    @mock.patch("carapp.db_models.User")
    def test_get_all_users(self, mock_user):
        with app.test_client() as client:
            mock_user.query.all.return_value = [
                TEST_USER,
            ]
            response = client.get("/users")
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.get_json(), dict)
            self.assertIsInstance(response.get_json()["Users"][0], dict)
            self.assertEqual(response.get_json()["Users"][0], TEST_USER)

    @unittest.skip("wip")
    @mock.patch("carapp.db_models.User")
    @mock.patch("carapp.db.session")
    def test_put_user(self, mock_session, mock_user):
        with app.test_client() as client:
            mock_user.query.filter_by.update.return_value = TESTER
            response = client.put("/user/100000", json=TESTER)
            self.assertIsNotNone(response.get_json())
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), TESTER)

    @unittest.skip("wip")
    @mock.patch("carapp.db_models.User")
    @mock.patch("carapp.db.session")
    def test_delete_user(self, mock_session, mock_user):
        with app.test_client() as client:
            mock_user.query.get.return_value = TEST_USER
            response = client.delete("/user/100000")
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 204)
            self.assertEqual(response.data, b"")

    @unittest.skip("wip")
    @mock.patch("carapp.db_models.User")
    def test_delete_user_failure(self, mock_user):
        with app.test_client() as client:
            mock_user.query.get.return_value = None
            response = client.delete("/user/100000")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.get_json(), {"Reason": "No User with id=100000"})

    @mock.patch("carapp.db_models.Car")
    def test_get_car(self, mock_car):
        with app.test_client() as client:
            mock_car.query.get.return_value = TEST_CAR
            response = client.get("/car/100000")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()["id"], 100000)

    @mock.patch("carapp.db_models.Car")
    def test_get_car_failure(self, mock_car):
        with app.test_client() as client:
            mock_car.query.get.return_value = None
            response = client.get("/car/100000")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 404)

    @mock.patch("carapp.db_models.Car")
    def test_get_all_cars(self, mock_car):
        with app.test_client() as client:
            FILTER = {"color": "White"}
            mock_car.query.filter_by(**FILTER).all.return_value = [
                TEST_CAR,
            ]
            response = client.get("/cars?color=White")
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.get_json(), dict)
            self.assertIsInstance(response.get_json()["Cars"][0], dict)
            self.assertEqual(response.get_json()["Cars"][0], TEST_CAR)

    @unittest.skip("wip")
    @mock.patch("carapp.db_models.Car")
    @mock.patch("carapp.db.session")
    def test_post_car(self, mock_session, mock_car):
        with app.test_client() as client:
            mock_car.return_value = TEST_CAR
            response = client.post("/car", json=TEST_CAR)
            self.assertIsNotNone(response.get_json())
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.get_json(), TEST_CAR)

    @unittest.skip("wip")
    @mock.patch("carapp.db_models.Car")
    @mock.patch("carapp.db.session")
    def test_put_car(self, mock_session, mock_car):
        with app.test_client() as client:
            mock_car.query.filter_by.update.return_value = TEST_CAR
            response = client.put("/car/1", json=TEST_CAR)
            self.assertIsNotNone(response.get_json())
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), TEST_CAR)

    @unittest.skip("wip")
    @mock.patch("carapp.db_models.Car")
    @mock.patch("carapp.db.session")
    def test_delete_car(self, mock_session, mock_car):
        with app.test_client() as client:
            mock_car.query.get.return_value = TEST_CAR
            response = client.delete("/car/100000")
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 204)
            self.assertEqual(response.data, b"")

    @unittest.skip("wip")
    @mock.patch("carapp.db_models.Car")
    def test_delete_car_failure(self, mock_car):
        with app.test_client() as client:
            mock_car.query.get.return_value = None
            response = client.delete("/car/100000")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.get_json(), {"Reason": "No Car with id=100000"})
