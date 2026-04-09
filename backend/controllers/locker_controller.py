import os
from flask import send_file, jsonify
from backend.models.locker import db_get_locker_with_booking

def get_locker_image(user_id, locker_id):
    locker = db_get_locker_with_booking(locker_id)
    if not locker:
        return jsonify({"error": "Locker not found or no active booking."}), 404

    image_path = locker['item_image_path']

    # Note: The keys from your db_get_locker_with_booking are sender_id and receiver_id
    if not (locker['sender_id'] == user_id or locker['receiver_id'] == user_id):
        return jsonify({"error": "You are not authorized to view this locker"}), 403

    if not image_path:
        return jsonify({"error": "No image for this locker"}), 404

    if not os.path.exists(image_path):
        return jsonify({"error": "Image file not found on disk"}), 404

    return send_file(image_path), 200


