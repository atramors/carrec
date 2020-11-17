import logging
from flask_restful import Resource
from carapp import api, db
from carapp.db_models import Car, User
from carapp.schemes import user_args, car_args, filter_args, user_schema, \
        car_schema
from webargs.flaskparser import use_kwargs
# from carapp import db_models

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s")
logger = logging.getLogger(__file__)


class UserData(Resource):
    def get(self, user_id):
        # Easier solution (check test.py)
        # user = db_models.User.query.get(user_id)
        user = User.query.get(user_id)
        if user is None:  # Comparision id of objects
            return {"Reason": "User not found", "User_id": user_id}, 404
        result = user_schema.dump(user)
        logger.info(f"\nUser with id={user_id} was called")
        return result

    def delete(self, user_id):
        user = User.query.get(user_id)
        result = user_schema.dump(user)
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
        # 0 or 1 (if updated)
        user_updated = User.query.filter_by(id=user_id).update(kwargs)
        if not user_updated:
            logger.error(f"\nNo User with id={user_id}")
            return {"Reason": "No such User", "User_id": user_id}, 404
        result = user_schema.load({**{"id": user_id}, **kwargs})
        db.session.commit()
        logger.info(f"\nUser with id={user_id} updated")
        return result, 200

    @use_kwargs(user_args)
    def post(self, **kwargs):
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        logger.info(f"\nUser with id={result['id']} created")
        return result, 201


class UserList(Resource):
    def get(self):
        users = User.query.all()
        list_of_users = [user_schema.dump(user) for user in users]
        logger.info(f"\nList of Users: {list_of_users}")
        return {"Users": list_of_users}


class CarData(Resource):
    def get(self, id):
        car = Car.query.get(id)
        if car is None:  # Comparision id of objects
            return {"Reason": "Car not found", "Car_id": id}, 404
        result = car_schema.dump(car)
        logger.info(f"\nCar with id={id} was called")
        return result

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
        logger.info(f"\nCar with id={result['id']} added")
        return result, 201


class CarList(Resource):
    @use_kwargs(filter_args, location="query")
    def get(self, **filter_args):
        car_list = Car.query.filter_by(**filter_args).all()
        list_of_cars = [car_schema.dump(car) for car in car_list]
        logger.info(f"\nGet {len(list_of_cars)} cars")
        return {"Cars": list_of_cars}


api.add_resource(UserData, "/user", "/user/<int:user_id>")
api.add_resource(UserList, "/users", methods=["GET"])
api.add_resource(CarData, "/car", "/car/<int:id>")
api.add_resource(CarList, "/cars", methods=["GET"])
