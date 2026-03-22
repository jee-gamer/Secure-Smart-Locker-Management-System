from flask import Blueprint, request, jsonify
from backend.controllers.user_controller import create_user, login, get_all_users

# THE PREFIXES ARE RIGHT HERE
user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/', methods=['GET'])
def list_users():
    all_users, status_code = get_all_users()
    return jsonify(all_users), status_code

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    result, status_code = create_user(username, password, role)

    if "error" in result:
        return jsonify(result), status_code

    return jsonify(result), status_code


@user_bp.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    result, status_code = login(username, password)

    if "error" in result:
        return jsonify(result), status_code

    return jsonify(result), status_code
