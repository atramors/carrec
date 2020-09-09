import requests
import carapp
import json
import logging
from carapp import api, app, bcrypt, db
from carapp.db_models import User, Car
from flask import request, jsonify
from flask_restful import Resource
from marshmallow import Schema, fields, validate, ValidationError
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs


logging.getLogger().setLevel(logging.WARNING)
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
        user = User.query.get(user_id)
        result = schema.dump(user)
        try:
            result, 200
        except AttributeError:
            logger.error(f"\nUser {result['username']}")
            return {"Reason": "User not found", "user_id": user_id}, 404
        logger.info(f"\nUser {result['username']} was called")
        return result

    @use_kwargs(user_args)
    def post(self, **kwargs):
        user = User(**kwargs)
        try:
            result = schema.dump(user)
        except ValidationError as error:
            logger.error(error.messages)
        db.session.add(user)
        db.session.commit()
        logger.info(f"\nUser {result['username']} was created.")
        return result, 201

    def delete(self, user_id):
        try:
            user = User.query.get(user_id)
            result = schema.dump(user) 
        except someError:
            return {"Reason": "No User with such id here!"}, 404
        db.session.delete(user)
        db.session.commit()
        logger.info(f"\nUser {result['username']} was deleted!")
        return "", 204


class UserList(Resource):
    def get(self):
        users = User.query.all()
        list_of_users = [schema.dump(user) for user in users]
        logger.info("\nAll users were called.")
        return list_of_users


api.add_resource(UserData, "/user", "/user/<int:user_id>")
api.add_resource(UserList, "/users")
