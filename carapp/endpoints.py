import requests
import carapp
import json
from carapp import api, app, bcrypt, db, db_models
from carapp.db_models import User, Car
from flask import request, jsonify
from flask_restful import Resource, marshal_with
from marshmallow import Schema, fields
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs

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
            return {"Reason": "User not found", "user_id": user_id}, 404
        return result

    @use_kwargs(user_args)
    def post(self, **kwargs):
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        result = schema.dump(user)
        return result, 201

    def delete(self, user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        result = schema.dump(user)
        return result["username"] + " was deleted!", 204


class UserList(Resource):
    def get(self):
        users = User.query.all()
        result = schema.dump(users)
        return result["username"]
            


api.add_resource(UserData, "/user", "/user/<int:user_id>")
api.add_resource(UserList, "/users")
