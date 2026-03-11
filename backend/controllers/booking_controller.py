from backend.models.booking import *
from backend.models.locker import is_occupied, set_status


def create_booking(user_id, receiver_id, locker_id):
    """
    Check if the locker is occupied or unoccupied
    Check if the locker is booked by different user
    """
    active = is_occupied(locker_id)

    if active:
        return {"message": "The locker is already occupied"}

    if not book(user_id, receiver_id, locker_id, item=1):
        return {"error": f"Failed to book locker: {locker_id}"}

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



