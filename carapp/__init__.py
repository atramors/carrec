import flask_bcrypt as fb
import flask_migrate
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from os.path import expanduser
from sqlalchemy import create_engine

app = Flask(__name__)
api = Api(app)
with open(expanduser("~/.pgpass"), "r") as f:
    host, port, database, user, password = f.read().split(":")
DB_ADD = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
app.config["SQLALCHEMY_DATABASE_URI"] = DB_ADD
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = fb.Bcrypt(app)
migrate = flask_migrate.Migrate(app, db)

from carapp import endpoints
