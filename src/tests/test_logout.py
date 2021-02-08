from flask_testing import TestCase

from main import create_app
from src.database.database import db


class LoginTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        return create_app()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_logout(self):
        data = {
            "email": "test@test.com",
            "password": "test",
            "username": "test"
        }

        self.client.post("/v1/auth/register", json=data)
        data = {"email": "test@test.com", "password": "test"}
        response = self.client.post("/v1/auth/login", json=data)
        data = {
            "flight_number": 6,
            "flight_name": "Air Asia",
            "departure": "BLR",
            "destination": "XLR",
            "fare_in_usd": 200,
            "scheduled_date": "02/08/2021",
            "scheduled_time": "02:21:24",
            "expected_arrival_date": "02/09/2021",
            "expected_arrival_time": "03:40:24"
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {response.json['token']}"
        }
        self.client.post("/v1/flight/add", json=data,
                         headers=headers)
        data = {
            "flight_number": 6
        }
        response = self.client.get("/v1/flight/search", json=data,
                                   headers=headers)
        self.assert200(response)
        self.assertEquals(data['flight_number'], response.json[0][
            'flight_flight_number'])
        response = self.client.post("/v1/auth/logout", headers=headers)
        self.assert200(response)
        self.assertEquals({"status": "Logged out."}, response.json)

    def test_access_after_logout(self):
        data = {
            "email": "test@test.com",
            "password": "test",
            "username": "test"
        }

        self.client.post("/v1/auth/register", json=data)
        data = {"email": "test@test.com", "password": "test"}
        response = self.client.post("/v1/auth/login", json=data)
        data = {
            "flight_number": 6,
            "flight_name": "Air Asia",
            "departure": "BLR",
            "destination": "XLR",
            "fare_in_usd": 200,
            "scheduled_date": "02/08/2021",
            "scheduled_time": "02:21:24",
            "expected_arrival_date": "02/09/2021",
            "expected_arrival_time": "03:40:24"
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {response.json['token']}"
        }
        self.client.post("/v1/flight/add", json=data,
                         headers=headers)
        data = {
            "flight_number": 6
        }
        response = self.client.get("/v1/flight/search", json=data,
                                   headers=headers)
        self.assert200(response)
        self.assertEquals(data['flight_number'], response.json[0][
            'flight_flight_number'])
        response = self.client.post("/v1/auth/logout", headers=headers)
        self.assert200(response)
        self.assertEquals({"status": "Logged out."}, response.json)
        response = self.client.get("/v1/flight/search", json=data,
                                   headers=headers)
        self.assert401(response)
        self.assertEquals({'message': 'Wrong credentials.'},
                          response.json)

    def test_logout_again(self):
        data = {
            "email": "test@test.com",
            "password": "test",
            "username": "test"
        }

        self.client.post("/v1/auth/register", json=data)
        data = {"email": "test@test.com", "password": "test"}
        response = self.client.post("/v1/auth/login", json=data)
        data = {
            "flight_number": 6,
            "flight_name": "Air Asia",
            "departure": "BLR",
            "destination": "XLR",
            "fare_in_usd": 200,
            "scheduled_date": "02/08/2021",
            "scheduled_time": "02:21:24",
            "expected_arrival_date": "02/09/2021",
            "expected_arrival_time": "03:40:24"
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {response.json['token']}"
        }
        self.client.post("/v1/flight/add", json=data,
                         headers=headers)
        data = {
            "flight_number": 6
        }
        response = self.client.get("/v1/flight/search", json=data,
                                   headers=headers)
        self.assert200(response)
        self.assertEquals(data['flight_number'], response.json[0][
            'flight_flight_number'])
        response = self.client.post("/v1/auth/logout", headers=headers)
        self.assert200(response)
        self.assertEquals({"status": "Logged out."}, response.json)
        response = self.client.post("/v1/auth/logout", headers=headers)
        self.assert200(response)
        self.assertEquals({'status': 'Already logged out.'}, response.json)
