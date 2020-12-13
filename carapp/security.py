import datetime
import jwt
from werkzeug.security import check_password_hash
from carapp import app, db_models
from flask import make_response, request
from functools import wraps

# app.config["SECRET_KEY"] = "thisissecret"


def token_required(any_function):
    @wraps(any_function)
    def wraped(self, *args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            return {"message": "Token is missing!"}, 401
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            self.user = db_models.User.query.filter_by(username=data["user"]).first()
        except jwt.exceptions.ExpiredSignatureError:
            return {"message": "Token is expired!"}, 401
        except jwt.exceptions.DecodeError:
            return {"message": "Token is wrong!"}, 401
        return any_function(self, *args, **kwargs)

    return wraped


@app.route("/login")
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response(
            "Could not verify. Probably no Authorization request header.",
            401,
            {"WWW-Authenticate": "Basic realm='Login required!'"},
        )
    user = db_models.User.query.filter_by(username=auth.username).first()
    if not user:
        return make_response(
            "Could not verify user",
            401,
            {"WWW-Authenticate": "Basic realm='Login required!'"},
        )
    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {
                "user": user.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            },
            app.config["SECRET_KEY"],
        )
        return {"token": token.decode("UTF-8")}
    return make_response(
        "Could not verify password",
        401,
        {"WWW-Authenticate": "Basic realm='Login required!'"},
    )
