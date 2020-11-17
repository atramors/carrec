from flask import jsonify
from carapp import app
from marshmallow import Schema, fields, validate


"""
Function to handle validation error.
"""


@app.errorhandler(422)
@app.errorhandler(400)
def handle_error(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify({"errors": messages}), err.code, headers
    else:
        return jsonify({"errors": messages}), err.code


"""
Schema for user-arguments parsing and validation of HTTP request objects.
"""

user_args = {
    "id": fields.Int(),
    "username": fields.Str(required=True),
    "password": fields.Str(required=True),
    "email": fields.Str(required=True),
    "account_type": fields.Str(required=True),
}


"""
Schema for car-arguments parsing and validation of HTTP request objects.
"""

car_args = {
    "car_title": fields.Str(required=True),
    "title": fields.Str(required=True),
    "condition": fields.Str(required=True),
    "body_type": fields.Str(required=True),
    "brand": fields.Str(required=True),
    "model": fields.Str(required=True),
    "year_of_production": fields.Str(required=True),
    "country_origin": fields.Str(required=True),
    "country_now": fields.Str(),
    "city": fields.Str(required=True),
    "mileage": fields.Str(required=True),
    "technical_condition": fields.Str(),
    "gear_box": fields.Str(required=True),
    "fuel_type": fields.Str(required=True),
    "engine": fields.Str(required=True),
    "color": fields.Str(required=True),
    "safety": fields.Str(),
    "wanted": fields.Str(required=True),
    "multimedia": fields.Str(required=True),
    "comfort": fields.Str(),
    "picture": fields.Str(required=True),
    "price": fields.Str(required=True),
    "drivetrain": fields.Str(required=True),
    "warranty": fields.Str(),
    "fuel_consumption": fields.Str(required=True),
    "date_added": fields.DateTime(),
    "user_id": fields.Int(),
}


"""
Schema for filter-arguments parsing and validation of HTTP request
objects (Query Params).
"""


# def must_exist(val):
#     if Car.query.filter_by(val).all() == []:
#         # Optionally pass a status_code
#         raise ValidationError("Car does not exist")


filter_args = {
    "car_title": fields.Str(validate=lambda value: len(value) > 0),
    "title": fields.Str(validate=lambda value: len(value) > 0),
    "condition": fields.Str(validate=lambda value: len(value) > 0),
    "body_type": fields.Str(validate=lambda value: len(value) > 0),
    "brand": fields.Str(validate=lambda value: len(value) > 0),
    "model": fields.Str(validate=lambda value: len(value) > 0),
    "year_of_production": fields.Str(validate=lambda value: len(value) > 0),
    "country_origin": fields.Str(validate=lambda value: len(value) > 0),
    "city": fields.Str(validate=lambda value: len(value) > 0),
    "mileage": fields.Str(validate=lambda value: len(value) > 0),
    "gear_box": fields.Str(validate=lambda value: len(value) > 0),
    "fuel_type": fields.Str(validate=lambda value: len(value) > 0),
    "engine": fields.Str(validate=lambda value: len(value) > 0),
    "color": fields.Str(validate=lambda value: len(value) > 0),
    "wanted": fields.Str(validate=lambda value: len(value) > 0),
    "picture": fields.Str(validate=lambda value: len(value) > 0),
    "price": fields.Str(validate=lambda value: len(value) > 0),
    "drivetrain": fields.Str(validate=lambda value: len(value) > 0),
    "fuel_consumption": fields.Str(validate=lambda value: len(value) > 0),
    "date_added": fields.DateTime(),
    "user_id": fields.Int(),
}


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str(validate=[validate.Length(min=3, max=20)])
    password = fields.Str(required=True)
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


user_schema = UserSchema()
car_schema = CarSchema()
