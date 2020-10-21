import flask_bcrypt as fb
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://karmaroma:'\
        'postgres@localhost:5432/new_carapp_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = fb.Bcrypt(app)

from carapp import endpoints
