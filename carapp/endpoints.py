import requests
import carapp
from flask import request
from flask_restful import Resource
from carapp import app, db, bcrypt


class UserData(Resource):
    def put(self, user_id):
        self.user = carapp.User(username,)

    def get(self, user_id):
        result = UserData.query.get(id=user_id)
        return {"user_id": user_id}

    def delete(self, user_id):
        pass


carapp.add_resource(UserData, "/user/<string:user_id>")
carapp.add_resource(CarData, "/user/<string:car_id>")
