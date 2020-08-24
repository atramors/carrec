import datetime
from carapp import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    account_type = db.Column(db.String(20), nullable=False)
    cars = db.relationship("Car", backref="author", lazy=True)

    def __repr__(self):
        return f"User({self.username}, {self.email})"


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_title = db.Column(db.String(80), nullable=False)
    car_info = db.Column(db.String(180), nullable=False)
    car_picture = db.Column(db.String(20), nullable=True)
    date_added = db.Column(
        db.DateTime(), nullable=False, default=datetime.datetime.utcnow
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Car({self.title}, {self.car_picture}, {self.date_added})"
