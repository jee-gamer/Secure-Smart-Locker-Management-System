from flask import Blueprint, request, jsonify
from backend.controllers.user_controller import create_user, login

# THE PREFIXES ARE RIGHT HERE
user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    result = create_user(username, password, role)

    if "error" in result:
        return jsonify(result), 409  # 409 Conflict

    return jsonify(result), 201


@user_bp.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    result = login(username, password)

    if "error" in result:
        return jsonify(result), 401  # 401 Unauthorized

    return jsonify(result), 200
