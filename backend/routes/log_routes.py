from flask import Blueprint, jsonify, request
from backend.controllers.log_controller import get_all_log_bookings, fetch_access_logs, create_locker_access_log

log_bp = Blueprint('logs', __name__, url_prefix='/logs')

@log_bp.route('/bookings', methods=['GET'])
def get_booking_logs():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    result, status_code = get_all_log_bookings(user_id)
    return jsonify(result), status_code

@log_bp.route('/access', methods=['GET'])
def get_access_logs():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    result, status_code = fetch_access_logs(user_id)
    return jsonify(result), status_code

@log_bp.route('/access/<int:locker_id>', methods=['POST'])
def log_locker_access(locker_id):
    data = request.get_json()
    user_id = data.get('user_id') if data else None
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    result, status_code = create_locker_access_log(user_id, locker_id)
    return jsonify(result), status_code
