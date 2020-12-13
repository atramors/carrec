import os
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate, MigrateCommand
from flask import Flask
from flask_restful import Api
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from os.path import expanduser
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()
app.config["SECRET_KEY"] = os.getenv("SECRET")

"""
Database config.
"""

with open(expanduser("~/.pgpass"), "r") as f:
    host, port, database, user, password = f.read().split(":")
DB_ADD = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
app.config["SQLALCHEMY_DATABASE_URI"] = DB_ADD
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

"""
Database migrations.
"""

migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)
manager.add_command("db", MigrateCommand)


from carapp import endpoints
