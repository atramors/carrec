import logging

import flask
import webargs.fields
from flask_restful import Resource
from marshmallow import Schema, fields, validate
from sqlalchemy import text
from webargs.flaskparser import use_kwargs

from carapp import api, app, bcrypt, db

# from carapp import db_models
from carapp.db_models import Car, User

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s")
logger = logging.getLogger(__file__)

user_args = {
    "id": webargs.fields.Int(),
    "username": webargs.fields.Str(required=True),
    "password": webargs.fields.Str(required=True),
    "email": webargs.fields.Str(required=True),
    "account_type": webargs.fields.Str(required=True),
}

car_args = {
    "car_title": webargs.fields.Str(required=True),
    "title": webargs.fields.Str(required=True),
    "condition": webargs.fields.Str(required=True),
    "body_type": webargs.fields.Str(required=True),
    "brand": webargs.fields.Str(required=True),
    "model": webargs.fields.Str(required=True),
    "year_of_production": webargs.fields.Str(required=True),
    "country_origin": webargs.fields.Str(required=True),
    "country_now": webargs.fields.Str(required=True),
    "city": webargs.fields.Str(required=True),
    "mileage": webargs.fields.Str(required=True),
    "technical_condition": webargs.fields.Str(required=True),
    "gear_box": webargs.fields.Str(required=True),
    "fuel_type": webargs.fields.Str(required=True),
    "engine": webargs.fields.Str(required=True),
    "color": webargs.fields.Str(required=True),
    "safety": webargs.fields.Str(required=True),
    "wanted": webargs.fields.Str(required=True),
    "multimedia": webargs.fields.Str(required=True),
    "comfort": webargs.fields.Str(required=True),
    "picture": webargs.fields.Str(required=True),
    "price": webargs.fields.Str(required=True),
    "drivetrain": webargs.fields.Str(required=True),
    "warranty": webargs.fields.Str(required=True),
    "fuel_consumption": webargs.fields.Str(required=True),
    "date_added": webargs.fields.DateTime(),
    "user_id": webargs.fields.Int(),
}


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str(validate=[validate.Length(min=3, max=20)])
    email = fields.Email(required=True)
    account_type = fields.Str(required=True)


class CarSchema(Schema):
    id = fields.Int()
    car_title = fields.Str(required=True)
    title = fields.Str(required=True)
    condition = fields.Str(required=True)
    body_type = fields.Str(required=True)
    brand = fields.Str(required=True)
    model = fields.Str(required=True)
    year_of_production = fields.Str(required=True)
    country_origin = fields.Str(required=True)
    country_now = fields.Str(required=True)
    city = fields.Str(required=True)
    mileage = fields.Str(required=True)
    technical_condition = fields.Str(required=True)
    gear_box = fields.Str(required=True)
    fuel_type = fields.Str(required=True)
    engine = fields.Str(required=True)
    color = fields.Str(required=True)
    safety = fields.Str(required=True)
    wanted = fields.Str(required=True)
    multimedia = fields.Str(required=True)
    comfort = fields.Str(required=True)
    picture = fields.Str(required=True)
    price = fields.Str(required=True)
    drivetrain = fields.Str(required=True)
    warranty = fields.Str(required=True)
    fuel_consumption = fields.Str(required=True)
    date_added = fields.DateTime()
    user_id = fields.Int()


schema = UserSchema()
car_schema = CarSchema()


class UserData(Resource):
    def get(self, user_id):
        # Easier solution (check test.py)
        # user = db_models.User.query.get(user_id)
        user = User.query.get(user_id)
        if user is None:  # Comparision id of objects
            return {"Reason": "User not found", "User_id": user_id}, 404
        result = schema.dump(user)
        logger.info(f"\nUser with id={user_id} was called")
        return result

    def delete(self, user_id):
        user = User.query.get(user_id)
        result = schema.dump(user)
        try:
            result["id"]
        except KeyError:
            logger.error(f"\nNo User with id={user_id}")
            return {"Reason": f"No User with id={user_id}"}, 404
        db.session.delete(user)
        db.session.commit()
        logger.info(f"\nUser with id={user_id} deleted")
        return "", 204

    @use_kwargs(user_args)
    def put(self, user_id, **kwargs):
        user_updated = User.query.filter_by(id=user_id).update(
            kwargs
        )  # 0 or 1 (if updated)
        if not user_updated:
            logger.error(f"\nNo User with id={user_id}")
            return {"Reason": "No such User", "User_id": user_id}, 404
        result = schema.load({**{"id": user_id}, **kwargs})
        db.session.commit()
        logger.info(f"\nUser with id={user_id} updated")
        return result, 200

    @use_kwargs(user_args)
    def post(self, **kwargs):
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        result = schema.dump(user)
        logger.info(f"\nUser with id={result['id']} created")
        return result, 201


class UserList(Resource):
    def get(self):
        users = User.query.all()
        list_of_users = [schema.dump(user) for user in users]
        logger.info(f"\nList of Users: {list_of_users}")
        return {"Users": list_of_users}


class CarData(Resource):
    #    def get(self):
    #        cars = Car.query.filter(Car.color == color.title()).all()
    #        result = [car_schema.dump(car) for car in cars]
    #        logger.info(f"\n{color.title()} cars called")
    #        return result
    #
    def delete(self, id):
        car = Car.query.get(id)
        result = car_schema.dump(car)
        try:
            result["id"]
        except KeyError:
            logger.error(f"\nNo Car with id={id}")
            return {"Reason": f"No Car with id={id}"}, 404
        db.session.delete(car)
        db.session.commit()
        logger.info(f"\nCar with id={id} deleted")
        return "", 204

    @use_kwargs(car_args)
    def put(self, id, **kwargs):
        # 0 or 1 (if updated)
        car_updated = Car.query.filter_by(id=id).update(kwargs)
        if not car_updated:
            logger.error(f"\nNo Car with id={id}")
            return {"Reason": "No such Car", "Car_id": id}, 404
        result = car_schema.load({**{"id": id}, **kwargs})
        db.session.commit()
        logger.info(f"\nCar with id={id} updated")
        return result, 200

    @use_kwargs(car_args)
    def post(self, **kwargs):
        car = Car(**kwargs)
        db.session.add(car)
        db.session.commit()

        result = car_schema.dump(car)
        # logger.info(f"\nCar for User with id=result["user_id"]["id"] added")
        return result, 201


class CarList(Resource):
    def get(self):
        cars = Car.query.all()
        list_of_cars = [car_schema.dump(car) for car in cars]
        return {"Cars": list_of_cars}


class CarFilter(Resource):
    pass


#     def get(self, col, search_data):
#         import pdb; pdb.set_trace()
#         cars = Car.query.filter(text(data_c).params(data_c = search_data)).all()
#         result = [car_schema.dump(car) for car in cars]
#         # logger.info(f"\nCar with id={result[id]} was called")
#         return result
#
#
api.add_resource(
    UserData, "/user", "/user/<int:user_id>", methods=["GET", "POST", "PUT", "DELETE"]
)
api.add_resource(UserList, "/users", methods=["GET"])
api.add_resource(
    CarData, "/car", "/car/<int:id>", methods=["GET", "POST", "PUT", "DELETE"]
)
api.add_resource(CarList, "/cars", methods=["GET"])
api.add_resource(CarFilter, "/cars/filters/<col>=<search_data>")
