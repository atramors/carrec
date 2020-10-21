import datetime
from carapp import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    account_type = db.Column(db.String(20), nullable=False)
    cars = db.relationship("Car", backref="user", lazy=True) 

    def __repr__(self):
        return f"User({self.username}, {self.email}, {self.account_type})"


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    car_title = db.Column(db.String(80), nullable=False)
    title = db.Column(db.Text, nullable=False)
    condition = db.Column(db.String(20), nullable=True)
    body_type = db.Column(db.String(30), nullable=True)
    brand = db.Column(db.String(20), nullable=True)
    model = db.Column(db.String(20), nullable=True)
    year_of_production = db.Column(db.String(20), nullable=True)
    country_origin = db.Column(db.String(20), nullable=True)
    country_now = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(20), nullable=True)
    mileage = db.Column(db.String(30), nullable=True)
    technical_condition = db.Column(db.Text, nullable=True)
    gear_box = db.Column(db.String(20), nullable=True)
    fuel_type = db.Column(db.String(20), nullable=True)
    engine = db.Column(db.String(50), nullable=True)
    color = db.Column(db.String(20), nullable=True)
    safety = db.Column(db.Text, nullable=True)
    wanted = db.Column(db.String(10), nullable=True)
    multimedia = db.Column(db.Text, nullable=True)
    comfort = db.Column(db.Text, nullable=True)
    picture = db.Column(db.String(20), nullable=True)
    price = db.Column(db.String(20), nullable=True)
    drivetrain = db.Column(db.String(20), nullable=True)
    warranty = db.Column(db.String(20), nullable=True)
    fuel_consumption = db.Column(db.String(80), nullable=True)
    date_added = db.Column(
        db.DateTime(), nullable=False, default=datetime.datetime.utcnow
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Car({self.title}, {self.picture}, {self.price})"
