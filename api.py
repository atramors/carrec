import requests
from datetime import datetime
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqllite///site.db"
db.create = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(180), nullable=True)
    image = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User({self.username}, {self.email}, {self.image})"


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    car_picture = db.Column(db.String(180), nullable=True)
    date_added = db.Column(db.Datetime(), nullable=False, default=datetime.utcnow)
    date_edited = db.Column(db.Datetime(), nullable=True)

    def __repr__(self):
        return f"User({self.car_picture}, {self.date_added})"




class UserData(Resource):
    # def put(self, user_id):
    #     pass

    def get(self, user_id):

        return {"user_id": user_id}

    # def delete(self, user_id):
    #     pass


api.add_resource(UserData, "/user/<string:user_id>")

if __name__ == "__main__":
    app.run(debug=True)
