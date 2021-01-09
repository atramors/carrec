import logging
import flask
import flask_login
from flask_restful import Resource
from carapp import api, app, auth, db, db_models, schemes, token_serializer
from webargs.flaskparser import use_kwargs
from werkzeug.security import generate_password_hash, check_password_hash

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s")
logger = logging.getLogger(__file__)


class UserSignUp(Resource):
    @use_kwargs(schemes.USER_ARGS)
    def post(self, **kwargs):
        hashed_password = generate_password_hash(kwargs["password"],
                                                 method="sha256")
        kwargs["password"] = hashed_password
        user = db_models.User(**kwargs)
        db.session.add(user)
        db.session.commit()
        result = schemes.USER_SCHEMA.dump(user)
        logger.info(f"\nUser with id={result['id']} created")
        return result, 201


class UserLogin(Resource):
    def post(self):
        check_auth = flask.request.authorization
        if not check_auth or not check_auth.username or not check_auth.password:
            return {"message": "Could not verify. Please Log In."}, 401

        user = db_models.User.query.filter_by(username=check_auth.username).first()
        if not user:
            return {"message": f"User {check_auth.username} doesn't exist."},
        401
        if check_password_hash(user.password, check_auth.password):
            token = token_serializer.dumps({"username": user.username}).decode("utf-8")
            flask_login.login_user(user)
            return {"message": f"Logged in as a {user.username}.", "token": token}

        return {"message": "Bad login"}, 401


class UserLogout(Resource):
    @auth.login_required
    def post(self):
        flask_login.logout_user()
        return flask.redirect("/login", code=302)


class UserData(Resource):
    @auth.login_required
    def get(self, user_id):
        user = db_models.User.query.get(user_id)
        if user is None:  # Comparision id of objects
            return {"Reason": "User not found", "User_id": user_id}, 404
        result = schemes.USER_SCHEMA.dump(user)
        logger.info(f"\nUser with id={user_id} was called")
        return result

    @auth.login_required
    def delete(self, user_id):
        user = db_models.User.query.get(user_id)
        result = schemes.USER_SCHEMA.dump(user)
        try:
            result["id"]
        except KeyError:
            logger.error(f"\nNo User with id={user_id}")
            return {"Reason": f"No User with id={user_id}"}, 404
        db.session.delete(user)
        db.session.commit()
        logger.info(f"\nUser with id={user_id} deleted")
        return "", 204

    @auth.login_required
    @use_kwargs(schemes.USER_ARGS)
    def put(self, user_id, **kwargs):
        hashed_password = generate_password_hash(kwargs["password"],
                                                 method="sha256")
        kwargs["password"] = hashed_password
        # 0 or 1 (if updated)
        user_updated = db_models.User.query.filter_by(id=user_id).update(kwargs)
        if not user_updated:
            logger.error(f"\nNo User with id={user_id}")
            return {"Reason": "No such User", "User_id": user_id}, 404
        result = schemes.USER_SCHEMA.load({**{"id": user_id}, **kwargs})
        db.session.commit()
        logger.info(f"\nUser with id={user_id} updated")
        return result, 200


class UserList(Resource):
    @auth.login_required
    def get(self):
        users = db_models.User.query.all()
        list_of_users = [schemes.USER_SCHEMA.dump(user) for user in users]
        logger.info(f"\nList of Users: {list_of_users}")
        return {"Users": list_of_users}


class CarData(Resource):
    def get(self, id):
        car = db_models.Car.query.get(id)
        if car is None:  # Comparision id of objects
            return {"Reason": "Car not found", "Car_id": id}, 404
        result = schemes.CAR_SCHEMA.dump(car)
        logger.info(f"\nCar with id={id} was called")
        return result

    @auth.login_required
    def delete(self, id):
        car = db_models.Car.query.get(id)
        result = schemes.CAR_SCHEMA.dump(car)
        try:
            result["id"]
        except KeyError:
            logger.error(f"\nNo Car with id={id}")
            return {"Reason": f"No Car with id={id}"}, 404
        db.session.delete(car)
        db.session.commit()
        logger.info(f"\nCar with id={id} deleted")
        return "", 204

    @auth.login_required
    @use_kwargs(schemes.CAR_ARGS)
    def put(self, id, **kwargs):
        # 0 or 1 (if updated)
        car_updated = db_models.Car.query.filter_by(id=id).update(kwargs)
        if not car_updated:
            logger.error(f"\nNo Car with id={id}")
            return {"Reason": "No such Car", "Car_id": id}, 404
        result = schemes.CAR_SCHEMA.load({**{"id": id}, **kwargs})
        db.session.commit()
        logger.info(f"\nCar with id={id} updated")
        return result, 200

    @auth.login_required
    @use_kwargs(schemes.CAR_ARGS)
    def post(self, **kwargs):
        car = db_models.Car(**kwargs)
        db.session.add(car)
        db.session.commit()
        result = schemes.CAR_SCHEMA.dump(car)
        logger.info(f"\nCar with id={result['id']} added")
        return result, 201


class CarList(Resource):
    @use_kwargs(schemes.FILTER_ARGS, location="query")
    def get(self, **filter_args):
        car_list = db_models.Car.query.filter_by(**filter_args).all()
        list_of_cars = [schemes.CAR_SCHEMA.dump(car) for car in car_list]
        logger.info(f"\nGet {len(list_of_cars)} cars")
        return {"Cars": list_of_cars}


api.add_resource(UserSignUp, "/signup", methods=["POST"])
api.add_resource(UserLogin, "/login", methods=["POST"])
api.add_resource(UserLogout, "/logout", methods=["POST"])
api.add_resource(UserData, "/user", "/user/<int:user_id>")
api.add_resource(UserList, "/users", methods=["GET"])
api.add_resource(CarData, "/car", "/car/<int:id>")
api.add_resource(CarList, "/cars", methods=["GET"])
