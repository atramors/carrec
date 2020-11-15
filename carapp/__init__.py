import flask_bcrypt as fb
from flask_migrate import Migrate
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from os.path import expanduser

app = Flask(__name__)
api = Api(app)
with open(expanduser("~/.pgpass"), "r") as f:
    host, port, database, user, password = f.read().split(":")
DB_ADD = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
app.config["SQLALCHEMY_DATABASE_URI"] = DB_ADD
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = fb.Bcrypt(app)
migrate = Migrate(app, db)

from carapp import endpoints
