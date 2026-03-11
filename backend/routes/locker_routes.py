from flask import Blueprint, jsonify
from backend.models.locker import db_get_all_lockers, db_get_locker_with_booking

locker_bp = Blueprint('lockers', __name__, url_prefix='/lockers')

@locker_bp.route('/', methods=['GET'])
def list_lockers():
    return jsonify(db_get_all_lockers()), 200

@locker_bp.route('/<int:locker_id>', methods=['GET'])
def get_locker(locker_id):
    locker = db_get_locker_with_booking(locker_id)
    if not locker:
        return jsonify({"error": "Locker not found"}), 404
    return jsonify(locker), 200
