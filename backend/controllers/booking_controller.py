from backend.models.booking import *
from backend.models.locker import is_occupied, set_status, set_image_path
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
        filename = secure_filename(item_image.filename)
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
    active = is_occupied(locker_id)

    if not active:
        return {"message": "The locker is not booked"}, 409

    if not unbook(user_id, locker_id):
        return {"error": f"Failed to unbook locker: {locker_id}"}, 400

    set_status(locker_id, "available")

    return {"message": f"Successfully unbooked locker: {locker_id}"}, 200

