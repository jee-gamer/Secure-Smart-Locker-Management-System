from backend.models.booking import *
from backend.models.locker import is_occupied, set_status, set_image_path
import os
from werkzeug.utils import secure_filename


def create_booking(user_id, receiver_id, locker_id, item_image):
    """
    Check if the locker is occupied or unoccupied
    Check if the locker is booked by different user
    """
    active = is_occupied(locker_id)

    if active:
        return {"message": "The locker is already occupied"}

    if not book(user_id, receiver_id, locker_id):
        return {"error": f"Failed to book locker: {locker_id}"}

    if item_image:
        filename = secure_filename(item_image.filename)
        upload_folder = os.path.join(os.path.dirname(__file__), '..', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        image_path = os.path.join(upload_folder, filename)
        item_image.save(image_path)
        set_image_path(locker_id, image_path)

    set_status(locker_id, "occupied")

    return {"message": f"Successfully booked locker: {locker_id}"}


def create_unbook(user_id, locker_id):
    active = is_occupied(locker_id)

    if not active:
        return {"message": "The locker is not booked"}

    if not unbook(user_id, locker_id):
        return {"error": f"Failed to unbook locker: {locker_id}"}

    set_status(locker_id, "available")

    return {"message": f"Successfully unbooked locker: {locker_id}"}



