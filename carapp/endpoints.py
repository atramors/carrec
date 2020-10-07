import requests
import carapp
import json
import logging
from carapp import api, app, bcrypt, db

# from carapp import db_models
from carapp.db_models import User, Car
from flask import request, jsonify
from flask_restful import Resource
from marshmallow import Schema, fields, validate, ValidationError
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s")
logger = logging.getLogger(__file__)

user_args = {
    "id": fields.Int(),
    "username": fields.Str(required=True),
    "password": fields.Str(validate=lambda p: len(p) >= 5),
    "email": fields.Str(required=True),
    "account_type": fields.Str(required=True),
}


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    password = fields.Str()
    email = fields.Email()
    account_type = fields.Str()


schema = UserSchema()


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
        user_updated = User.query.filter_by(id=user_id).update(kwargs) # 0 or 1 (if updated)
        if not user_updated:
            logger.error(f"\nNo User with id={user_id}")
            return {"Reason": "No such User", "User_id": user_id}, 404
        result = schema.load({**{"id": user_id}, **kwargs})
        db.session.commit()
        logger.info(f"\nUser with id={user_id} updated")
        return result, 200


class UserList(Resource):
    def get(self):
        users = User.query.all()
        list_of_users = [schema.dump(user) for user in users]
        logger.info(f"\nList of Users: {list_of_users}")
        return {"Users": list_of_users}

    @use_kwargs(user_args)
    def post(self, **kwargs):
        user = User(**kwargs)
        result = schema.dump(user)
        db.session.add(user)
        db.session.commit()
        logger.info(f"\nUser with id={result['id']} created")
        return result, 201


api.add_resource(UserData, "/users/<int:user_id>")
api.add_resource(UserList, "/users")
