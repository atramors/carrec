import requests
from datetime import datetime
from models import User, Car


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    date_added = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    date_edited = db.Column(db.DateTime(), nullable=True)

    def __repr__(self):
        return f"User({self.car_picture}, {self.date_added})"


if __name__ == "__main__":
    app.run(debug=True)
