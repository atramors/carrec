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


class UserData(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        try:
            result = (
                {
                    "username": user.username,
                    "email": user.email,
                    "account_type": user.account_type,
                },
                200,
            )
        except AttributeError:
            return {"Reason": "User not found", "user_id": user_id}, 404
        return result
        
    @use_kwargs(user_args)
    def post(self, **kwargs):
        user = User(**kwargs)
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

    def delete(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        return (f"{user.username} was gone!", 204)


class UserList(Resource):
    @use_args(user_args)
    def get(self, args, **kwargs):
        users = User.query.order_by(username=args["username"]).all()
        
        for i in range(len(users)):
            return users[i].username
        # return users


api.add_resource(UserData, "/user", "/user/<int:user_id>")
api.add_resource(UserList, "/users")
