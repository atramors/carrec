import unittest
from unittest import mock
from carapp import app, db, db_models, endpoints


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
    def test_get_user(self, MockUser):
        with app.test_client() as client:
            MockUser.query.get.return_value = TEST_USER
            response = client.get("/user/100000")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()["id"], 100000)

    @mock.patch("carapp.db_models.User")
    def test_get_user_failure(self, MockUser):
        with app.test_client() as client:
            MockUser.query.get.return_value = None
            response = client.get("/user/100000")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 404)

    @mock.patch("carapp.db_models.User")
    def test_get_all_users(self, MockUser):
        with app.test_client() as client:
            MockUser.query.all.return_value = [
                TEST_USER,
            ]
            response = client.get("/users")
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.get_json(), dict)
            self.assertIsInstance(response.get_json()["Users"][0], dict)
            self.assertEqual(response.get_json()["Users"][0], TEST_USER)

    @mock.patch("carapp.db_models.User")
    @mock.patch("carapp.db.session")
    def test_post_user(self, MockSession, MockUser):
        TESTER = {
            "id": 100000,
            "username": "Barbie",
            "password": "12134",
            "email": "Barbie@satana666.com",
            "account_type": "test-client",
        }
        with app.test_client() as client:
            MockUser.return_value = TESTER
            response = client.post("/user", json=TESTER)
            self.assertIsNotNone(response.get_json())
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.get_json(), TESTER)

    @mock.patch("carapp.db_models.User")
    @mock.patch("carapp.db.session")
    def test_put_user(self, MockSession, MockUser):
        TESTER = {
            "id": 100000,
            "username": "Barbie",
            "password": "12134",
            "email": "Barbie@satana666.com",
            "account_type": "test-client",
        }
        with app.test_client() as client:
            MockUser.query.filter_by.update.return_value = TESTER
            response = client.put("/user/100000", json=TESTER)
            self.assertIsNotNone(response.get_json())
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), TESTER)

    @mock.patch("carapp.db_models.User")
    @mock.patch("carapp.db.session")
    def test_delete_user(self, MockSession, MockUser):
        with app.test_client() as client:
            MockUser.query.get.return_value = TEST_USER
            response = client.delete("/user/100000")
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 204)
            self.assertEqual(response.data, b"")

    @mock.patch("carapp.db_models.User")
    def test_delete_user_failure(self, MockUser):
        with app.test_client() as client:
            MockUser.query.get.return_value = None
            response = client.delete("/user/100000")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.get_json(), {"Reason": "No User with id=100000"})

    @mock.patch("carapp.db_models.Car")
    def test_get_car(self, MockCar):
        with app.test_client() as client:
            MockCar.query.get.return_value = TEST_CAR
            response = client.get("/car/100000")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()["id"], 100000)

    @mock.patch("carapp.db_models.Car")
    def test_get_car_failure(self, MockCar):
        with app.test_client() as client:
            MockCar.query.get.return_value = None
            response = client.get("/car/100000")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 404)

    @mock.patch("carapp.db_models.Car")
    def test_get_all_cars(self, MockCar):
        with app.test_client() as client:
            FILTER = {"color": "White"}
            MockCar.query.filter_by(**FILTER).all.return_value = [
                TEST_CAR,
            ]
            response = client.get("/cars?color=White")
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.get_json(), dict)
            self.assertIsInstance(response.get_json()["Cars"][0], dict)
            self.assertEqual(response.get_json()["Cars"][0], TEST_CAR)

    @mock.patch("carapp.db_models.Car")
    @mock.patch("carapp.db.session")
    def test_post_car(self, MockSession, MockCar):
        CAR = {
            "id": 100000,
            "car_title": "Supercar",
            "title": "Supercar_3000",
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
            "date_added": "2020-10-21 15:02:54.770364",
            "user_id": 999,
        }
        with app.test_client() as client:
            MockCar.return_value = CAR
            response = client.post("/car", json=CAR)
            self.assertIsNotNone(response.get_json())
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.get_json(), CAR)

    @mock.patch("carapp.db_models.Car")
    @mock.patch("carapp.db.session")
    def test_put_car(self, MockSession, MockCar):
        CAR = {
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
            "date_added": "2020-10-21 15:02:54.770364",
            "user_id": 999,
        }
        with app.test_client() as client:
            MockCar.query.filter_by.update.return_value = CAR
            response = client.put("/car/100000", json=CAR)
            self.assertIsNotNone(response.get_json())
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), CAR)

    @mock.patch("carapp.db_models.Car")
    @mock.patch("carapp.db.session")
    def test_delete_car(self, MockSession, MockCar):
        with app.test_client() as client:
            MockCar.query.get.return_value = TEST_CAR
            response = client.delete("/car/100000")
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 204)
            self.assertEqual(response.data, b"")

    @mock.patch("carapp.db_models.Car")
    def test_delete_car_failure(self, MockCar):
        with app.test_client() as client:
            MockCar.query.get.return_value = None
            response = client.delete("/car/100000")
            self.assertIsNotNone(response)
            self.assertIsInstance(response.get_json(), dict)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.get_json(), {"Reason": "No Car with id=100000"})
