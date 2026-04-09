from backend.models.booking import get_all_bookings
from backend.models.user import db_get_user_by_id
from backend.models.access_log import get_all_access_logs, log_access
from backend.models.locker import db_get_locker_with_booking

def create_locker_access_log(user_id, locker_id):
    locker = db_get_locker_with_booking(locker_id)

    if locker and (locker['sender_id'] == user_id or locker['receiver_id'] == user_id):
        action = "opened"
    else:
        # Check if they are an admin
        user = db_get_user_by_id(user_id)
        if user and user.get('role') == 'admin':
            action = "opened (admin)"
        else:
            action = "unauthorized_attempt"

    log_access(user_id, locker_id, action)
    return {"message": "Access logged successfully"}, 200

def get_all_log_bookings(user_id):
    user = db_get_user_by_id(user_id)
    if not user or user.get('role') != 'admin':
        return {"error": "Unauthorized. Admin access required."}, 403

    bookings = get_all_bookings()
    if bookings is None:
        return {"error": "Failed to retrieve bookings"}, 500
    return {"data": bookings}, 200

def fetch_access_logs(user_id):
    user = db_get_user_by_id(user_id)
    if not user or user.get('role') != 'admin':
        return {"error": "Unauthorized. Admin access required."}, 403

    logs = get_all_access_logs()
    return {"data": logs}, 200
