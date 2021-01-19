from carapp import auth, db_models, login_manager, token_serializer


@login_manager.user_loader
def user_loader(user_id):
    return db_models.User.query.get(user_id)


@auth.verify_token
def verify_token(token):
    try:
        data = token_serializer.loads(token)
    except:
        return False
    if "username" in data:
        return data["username"]
