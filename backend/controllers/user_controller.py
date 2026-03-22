from backend.models.user import *
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(username, password, role='user'):
    user = db_get_user_by_username(username)

    if user:
        return {"error": "This username is already registered"}, 409
    hashed = generate_password_hash(password)

    db_create_user(username, hashed, role)
    return {"message": "User created successfully"}, 200

def login(username, password):
    user = db_get_user_by_username(username)
    if not user:
        return {"error": "User does not exist"}, 401

    if not check_password_hash(user["password"], password):
        return {"error": "Incorrect password"}, 401

    return {
        "message": "Logged in successfully",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"]
        }
    }, 200

def get_all_users():
    users = db_get_all_users()

    if not users:
        return {"message": "No users found"}, 404

    return users, 200
