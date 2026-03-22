import uuid

from backend.models.booking import *
from backend.models.locker import is_occupied, set_status, set_image_path, db_get_locker_with_booking
import os
from werkzeug.utils import secure_filename


def create_booking(user_id, receiver_id, locker_id, item_image):
    """
    Check if the locker is occupied or unoccupied
    Check if the locker is booked by different user
    """
    print(f"--- Create Booking ---")
    print(f"User: {user_id}, Receiver: {receiver_id}, Locker: {locker_id}")
    print(f"Received item_image: {item_image}")

    active = is_occupied(locker_id)

    if active:
        return {"message": "The locker is already occupied"}, 409

    if not book(user_id, receiver_id, locker_id):
        return {"error": f"Failed to book locker: {locker_id}"}, 400

    if item_image:
        original_filename = secure_filename(item_image.filename)
        _, ext = os.path.splitext(original_filename)
        filename = str(uuid.uuid4()) + ext

        # Correctly resolve the project's root directory for the uploads folder
        upload_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploads'))
        print(f"Upload folder target: {upload_folder}")
        os.makedirs(upload_folder, exist_ok=True)
        image_path = os.path.join(upload_folder, filename)
        print(f"Saving image to: {image_path}")
        item_image.save(image_path)
        set_image_path(locker_id, image_path)
        print("Image path set in DB.")

    set_status(locker_id, "occupied")
    print("--- Booking Complete ---")
    return {"message": f"Successfully booked locker: {locker_id}"}, 200


def create_unbook(user_id, locker_id):
    locker = db_get_locker_with_booking(locker_id)

    active = is_occupied(locker_id)
    if not active:
        return {"message": "The locker is not booked"}, 409

    authorized = locker['sender_id'] == user_id
    if not authorized:
        return {"message": "You are not the locker booker"}, 403

    if not unbook(user_id, locker_id):
        return {"error": f"Failed to unbook locker: {locker_id}"}, 400

    image_path = locker['item_image_path']

    if image_path and os.path.exists(image_path):
        try:
            os.remove(image_path)
            print(f"Deleted old image: {image_path}")
        except OSError as e:
            print(f"Error deleting file {image_path}: {e}")

    # Clear the image path in the database and set status to available
    set_image_path(locker_id, None)
    set_status(locker_id, "available")

    return {"message": f"Successfully unbooked locker: {locker_id}"}, 200

