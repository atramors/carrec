import requests
import carapp
from carapp import api, app, bcrypt, db, db_models
from carapp.db_models import User, Car
from flask import request
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs, parser

user_detail_args = {
    "id": fields.Int(),
    "username": fields.Str(required=True),
    "password": fields.Str(validate=lambda p: len(p) >= 5),
    "email": fields.Str(required=True),
    "account_type": fields.Str(required=True),
}


class UserData(Resource):
    @use_kwargs(user_detail_args)
    def get(self, args, uid):
        result = User.query.get(id=uid)
        return result

    @use_kwargs(user_detail_args)
    def post(self, args, uid):
        user = User(
            id=uid,
            username=args["username"],
            password=args["password"],
            email=args["email"],
            account_type=args["account_type"],
        )
        db.session.add(user)
        db.session.commit()
        return user, 201


api.add_resource(UserData, "/user/<int:uid>")
