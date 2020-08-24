import flask_bcrypt as fb
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)
bcrypt = fb.Bcrypt(app)

from carapp import endpoints
