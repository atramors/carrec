import flask
import flask_login
from . import app, auth, db_models, login_manager, token_serializer
from flask import make_response, request
from werkzeug.security import check_password_hash


@login_manager.user_loader
def user_loader(user_id):
    user = db_models.User.query.get(user_id)
    if not user:
        return None

    return user


# @login_manager.request_loader
# def request_loader(request):
#     username = request.authorization.username
#     # import pdb; pdb.set_trace()
#     user = db_models.User.query.filter_by(username=username).first()
#     if not user:
#         return None

    # user.is_authenticated = check_password_hash(
    #    user.password, request.authorization.password
    # )
#     return user


@auth.verify_token
def verify_token(token):
    try:
        data = token_serializer.loads(token)
    except:  # noqa: E722
        return False
    if 'username' in data:
        return data['username']


@app.route("/")
def index():
    if "_user_id" in flask.session:
        return "Logged in as " + flask_login.current_user.username

    return "You are not logged in!"


@app.route("/login", methods=["GET", "POST"])
def login():
    check_auth = request.authorization
    if not check_auth or not check_auth.username or not check_auth.password:
        return make_response(
            "Could not verify. Please Log In.",
            401,
            {"WWW-Authenticate": "Basic realm='Login required!'"},
        )
    user = db_models.User.query.filter_by(username=check_auth.username).first()
    if not user:
        return make_response(
            "Could not verify user",
            401,
            {"WWW-Authenticate": "Basic realm='Login required!'"},
        )
    if check_password_hash(user.password, check_auth.password):
        token = token_serializer.dumps({'username': user.username}).decode('utf-8')
        flask_login.login_user(user)
        return {"message": f"Logged in as a {user.username}.", "token": token}

    return 401, {"message": "Bad login"}


@app.route("/protected")
@flask_login.login_required
def protected():
    return "Logged in as " + flask_login.current_user.username


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for("index"))
