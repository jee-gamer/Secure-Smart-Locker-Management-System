from flask import Blueprint, request, jsonify
from backend.controllers.booking_controller import create_booking, create_unbook
from backend.models.booking import get_all_active_bookings

booking_bp = Blueprint('bookings', __name__, url_prefix='/bookings')

@booking_bp.route('/', methods=['POST'])
def book():
    print("--- BOOK ROUTE ---")
    print("Request Headers:", request.headers)
    user_id = request.form.get('user_id')
    receiver_id = request.form.get('receiver_id')
    locker_id = request.form.get('locker_id')
    item_image = request.files.get('item_image')

    if not user_id or not receiver_id or not locker_id:
        return jsonify({"error": "user_id, receiver_id, and locker_id are required"}), 400

    result = create_booking(user_id, receiver_id, locker_id, item_image)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 201


@booking_bp.route('/', methods=['DELETE'])
def unbook():
    data = request.get_json()
    user_id = data.get('user_id')
    locker_id = data.get('locker_id')

    if not user_id or not locker_id:
        return jsonify({"error": "user_id and locker_id are required"}), 400

    result = create_unbook(user_id, locker_id)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200


@booking_bp.route('/get-active', methods=['GET'])
def get_active():

    active_bookings = get_all_active_bookings()

    return jsonify(active_bookings), 200
