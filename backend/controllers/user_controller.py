from ..models.user import *
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(username, password, role='user'):
    user = db_get_user_by_username(username)

    if user:
        return {"error": "This username is already registered"}
    hashed = generate_password_hash(password)

    db_create_user(username, password, role)
    return {"message": "User created successfully"}

def login(username, password):
    user = db_get_user_by_username(username)
    if not user:
        return {"error": "User does not exist"}

    if not check_password_hash(user.password, password):
        return {"error": "Incorrect password"}

    return {"message": "Logged in successfully"}
