import requests
import carapp
import json
from carapp import api, app, bcrypt, db, db_models
from carapp.db_models import User, Car
from flask import request, jsonify
from flask_restful import Resource, abort
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs

user_args = {
    "id": fields.Int(),
    "username": fields.Str(required=True),
    "password": fields.Str(validate=lambda p: len(p) >= 5),
    "email": fields.Str(required=True),
    "account_type": fields.Str(required=True),
}


class UserData(Resource):
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        return (
            {
                "username": user.username,
                "email": user.email,
                "account_type": user.account_type,
            },
            200,
        )

    @use_args(user_args)
    def post(self, args, **kwargs):
        user = User(
            id=args["id"],
            username=args["username"],
            password=args["password"],
            email=args["email"],
            account_type=args["account_type"],
        )
        db.session.add(user)
        db.session.commit()

        return (
            {
                "username": user.username,
                "email": user.email,
                "account_type": user.account_type,
            },
            201,
        )
"""
    @use_args(user_args)
    def delete(self, user_id, args, **kwargs):
        user = User.query.filter_by(id=args["id"]).first()
        db.session.delete(user)
        db.session.commit()

        return f"User with Username {user.username} was deleted!", 204


class UserList(Resource):
    # @use_args(user_args)
    def get(self, args):
        users = User.query.all()
        # for i in range(len(users)):
        #     return users[i]
        return users
"""

api.add_resource(UserData, "/user/<int:user_id>")
api.add_resource(UserList, "/users")
